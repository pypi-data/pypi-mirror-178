
import weakref

from c3.constants import *
from c3.errors import *
from c3 import textfiles
from c3 import structure
from c3 import getpassword

from c3.structure import AttrDict

# --- Data output classes ---
# These are attached to the CEs as properties .pub. .priv. .both.  so e.g. ce.both.as_text()
# so we can go e.g. ce.pub.as_text(),  ce.both.as_binary(),

# Note: textfiles.load_files is the inverse of the write_text_file functions here.

class CeOutPub(object):
    def __init__(self, ce_parent):
        self.ce = ce_parent

    def as_binary(self):
        return self.ce.pub_block

    def as_text(self, vis_map=None, desc=""):
        return textfiles.make_pub_txt_str_ce(self.ce, desc, vis_map)

    def write_text_file(self, filename, vis_map=None, desc=""):
        txt = self.as_text(vis_map, desc)
        with open(filename+".public.b64.txt", "wt") as f:
            f.write(txt)
        return


class CeOutPriv(object):
    def __init__(self, ce_parent):
        self.ce = ce_parent

    def as_binary(self):
        if not self.ce.epriv_block:
            raise OutputError("Please encrypt() or nopassword() the private key")
        return self.ce.epriv_block

    def as_text(self, vis_map=None, desc=""):
        if not self.ce.epriv_block:
            raise OutputError("Please encrypt() or nopassword() the private key")
        return textfiles.make_priv_txt_str_ce(self.ce, desc)  # note vis_map not used

    def write_text_file(self, filename, vis_map=None, desc=""):
        txt = self.as_text(vis_map, desc)
        with open(filename+".PRIVATE.b64.txt", "wt") as f:
            f.write(txt)


class CeOutBoth(object):
    def __init__(self, ce_parent):
        self.ce = ce_parent

    def as_binary(self):
        if not self.ce.epriv_block:
            raise OutputError("Please encrypt() or nopassword() the private key")
        return structure.combine_binary_pub_priv(self.ce.pub_block, self.ce.epriv_block)

    def as_text(self, vis_map=None, desc=""):
        if not self.ce.epriv_block:
            raise OutputError("Please encrypt() or nopassword() the private key")
        pub_str = textfiles.make_pub_txt_str_ce(self.ce, desc, vis_map)
        priv_str = textfiles.make_priv_txt_str_ce(self.ce, desc)
        return "\n" + pub_str + "\n" + priv_str + "\n"

    def write_text_file(self, filename, vis_map=None, desc=""):
        txt = self.as_text(vis_map, desc)
        with open(filename+".b64.txt", "wt") as f:
            f.write(txt)



class CertEntry(object):
    def __init__(self, parent):
        self.parent = weakref.ref(parent)   # pointer to the SignVerify object whose registry(s) we live in
        self.pub_type = 0                   # tag value e.g. PUB_CSR
        self.name = ""

        self.pub_text = ""
        self.epriv_text = ""

        self.pub_block = b""
        self.epriv_block = b""          # bytes of packed PRIV_CRCWRAPPED structure

        self.priv_d = {}                # unpacked PRIV_CRCWRAPPED structure
        self.priv_key_bytes = b""       # actual private key bytes (priv_d.priv_data)

        self.payload = b""              # this or cert, depending on pub_type
        self.cert = {}                  # aka chain[0]
        self.sig = b""

        self.chain = []

        self.vis_map = {}
        self.default_vismap = dict(schema=CERT_SCHEMA,
                                   field_map=["subject_name", "expiry_date", "issued_date", "cert_type"])
        # Output class instances, so user can go ce.pub.as_text(), ce.both.as_binary() etc.
        self.pub = CeOutPub(self)
        self.priv = CeOutPriv(self)
        self.both = CeOutBoth(self)

    # ============== Metadata access functions =============================================

    def chain_certs(self):
        return reversed([i["cert"] for i in self.chain if "cert" in i])

    def chain_types(self):          # NOTE This doesn't include linked-by-name and it needs to.D
        return [i.get("cert_type", "") for i in self.chain_certs()]

    def chain_names(self):
        return [i["subject_name"] for i in self.chain_certs()]


    # ============== Private key encrypt ===================================================

    def private_key_encrypt_sanity_checks(self):
        if not self.priv_key_bytes:
            raise ValueError("CE has no private key bytes")

    def private_key_encrypt(self, password):
        self.private_key_encrypt_sanity_checks()
        epriv_bytes = self.parent().pass_protect.SinglePassEncrypt(self.priv_key_bytes, password)
        self.epriv_block = structure.make_priv_block(epriv_bytes, bare=False)
        return

    def private_key_encrypt_user(self):
        self.private_key_encrypt_sanity_checks()
        prompt1 = "Enter password to set on private key > "
        prompt2 = "Re-enter private key password        > "
        passw = getpassword.get_double_enter_setting_password(prompt1, prompt2)
        if not passw:
            raise ValueError("No password supplied, exiting")
        epriv_bytes = self.parent().pass_protect.SinglePassEncrypt(self.priv_key_bytes, passw)
        self.epriv_block = structure.make_priv_block(epriv_bytes, bare=False)

    def private_key_set_nopassword(self):
        self.private_key_encrypt_sanity_checks()
        self.epriv_block = structure.make_priv_block(self.priv_key_bytes, bare=True)

    # ============== Private key decrypt ===================================================

    # out: True - dealt with it (BARE), False= password still needs doing.
    def private_key_decrypt_sanity_checks(self):
        # already have priv_d from load() calling structure.load_priv_block
        if self.priv_d.priv_type == PRIVTYPE_BARE:    # just in case the user calls us when they're not
            self.priv_key_bytes = self.priv_d.priv_data  # supposed to (e.g. a bare key was loaded)
            return True   # be good about it anyway so the user doesn't have to special case things.

        if self.priv_d.priv_type != PRIVTYPE_PASS_PROTECT:
            raise StructureError("Private key is encrypted with an unknown encryption")
        # todo: we dont support this here yet
        if self.parent().pass_protect.DualPasswordsNeeded(self.priv_d.priv_data):
            raise NotImplementedError("Private key wants dual passwords")
        return False

    def private_key_decrypt(self, password):
        if self.private_key_decrypt_sanity_checks():    # true = we're done (e.g BARE)
            return
        priv_ret = self.parent().pass_protect.SinglePassDecrypt(self.priv_d.priv_data, password)
        self.priv_key_bytes = priv_ret

    def private_key_decrypt_user(self):
        if self.private_key_decrypt_sanity_checks():     # true = we're done (e.g BARE)
            return
        # --- Try password from environment variables ---
        passw = getpassword.get_env_password()
        if passw:
            priv_ret = self.parent().pass_protect.SinglePassDecrypt(self.priv_d.priv_data, passw)
            # Note exceptions are propagated right out here, its an exit if this decrypt fails.
            self.priv_key_bytes = priv_ret
            return

        # --- Try password from user ---
        prompt = "Password to unlock private key: "
        priv_ret = b""
        while not priv_ret:
            passw = getpassword.get_enter_password(prompt)
            if not passw:
                raise ValueError("No password supplied, exiting")

            try:
                priv_ret = self.parent().pass_protect.SinglePassDecrypt(self.priv_d.priv_data, passw)
            except Exception as e:
                print("Failed decrypting private key: ", str(e))
                continue        # let user try again
        self.priv_key_bytes = priv_ret
        return

    # Note: there is no inverse for private_key_nopassword because
    #       incoming BARE keys are handled directly by load()

    def private_key_unload(self):
        self.priv_key_bytes = b""

