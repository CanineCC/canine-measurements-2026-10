# Independent check of a CAI-delivery signature, without the reference program: canonicalise the payload
# (RFC 8785 style: sorted keys, no whitespace, shortest number form), then Ed25519-verify the signature
# against the public key named by keyId in the key set. Prints the sha256 of the canonical payload too.
import sys, json, base64, hashlib, math
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

def b64u(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

def num(x):
    if isinstance(x, bool): return "true" if x else "false"
    if isinstance(x, int): return str(x)
    if math.isfinite(x) and x == int(x) and abs(x) < 1e21: return str(int(x))
    r = repr(x)
    return r

def canon(o):
    if o is None: return "null"
    if isinstance(o, (bool, int, float)): return num(o)
    if isinstance(o, str): return json.dumps(o, ensure_ascii=False)
    if isinstance(o, list): return "[" + ",".join(canon(v) for v in o) + "]"
    keys = sorted(o.keys(), key=lambda k: k.encode("utf-16-be"))
    return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + canon(o[k]) for k in keys) + "}"

pkg = json.load(open(sys.argv[1], encoding="utf-8"))
keys = json.load(open(sys.argv[2], encoding="utf-8"))["keys"]
sig = pkg["signature"]
key = next(k for k in keys if k["keyId"] == sig["keyId"])
data = canon(pkg["payload"]).encode("utf-8")
print("canon", sig["canon"], "| keyId", sig["keyId"], "| key status", key["status"])
print("sha256(canonical payload)", hashlib.sha256(data).hexdigest())
try:
    Ed25519PublicKey.from_public_bytes(b64u(key["publicKey"])).verify(b64u(sig["value"]), data)
    print("Ed25519 signature: VALID")
except InvalidSignature:
    print("Ed25519 signature: INVALID"); sys.exit(1)
