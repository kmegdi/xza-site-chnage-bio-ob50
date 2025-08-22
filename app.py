from flask import Flask, request, render_template
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

app = Flask(__name__)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Key و IV
key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
url_bio = "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo"
freefire_version = "OB50"

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\ndata.proto\"\xbb\x01\n\x04\x44\x61ta\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05\x12\x1e\n\x07\x66ield_5\x18\x05 \x01(\x0b\x32\r.EmptyMessage\x12\x1e\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\r.EmptyMessage\x12\x0f\n\x07\x66ield_8\x18\x08 \x01(\t\x12\x0f\n\x07\x66ield_9\x18\t \x01(\x05\x12\x1f\n\x08\x66ield_11\x18\x0b \x01(\x0b\x32\r.EmptyMessage\x12\x1f\n\x08\x66ield_12\x18\x0c \x01(\x0b\x32\r.EmptyMessage\"\x0e\n\x0c\x45mptyMessageb\x06proto3'
)
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data1_pb2', _globals)
Data = _sym_db.GetSymbol('Data')
EmptyMessage = _sym_db.GetSymbol('EmptyMessage')

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route("/", methods=["GET", "POST"])
def home():
    message = None
    if request.method == "POST":
        jwt_token = request.form.get("jwt")
        bio = request.form.get("bio")

        try:
            # تجهيز Data
            data = Data()
            data.field_2 = 17
            data.field_5.CopyFrom(EmptyMessage())
            data.field_6.CopyFrom(EmptyMessage())
            data.field_8 = bio
            data.field_9 = 1
            data.field_11.CopyFrom(EmptyMessage())
            data.field_12.CopyFrom(EmptyMessage())

            # Serialize + Encrypt
            data_bytes = data.SerializeToString()
            padded_data = pad(data_bytes, AES.block_size)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            encrypted_data = cipher.encrypt(padded_data)

            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "X-Unity-Version": "2018.4.11f1",
                "X-GA": "v1 1",
                "ReleaseVersion": freefire_version,
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Dalvik/2.1.0 (Linux; Android 11)",
                "Host": "clientbp.ggblueshark.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip"
            }

            res = requests.post(url_bio, headers=headers, data=encrypted_data)

            if res.status_code == 200:
                message = f"✅ البايو الجديد تم تحديثه بنجاح!\n\n📝 {bio}"
            else:
                message = f"❌ خطأ: {res.status_code} - {res.text}"

        except Exception as e:
            message = f"⚠️ خطأ داخلي: {str(e)}"

    return render_template("index.html", message=message)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)