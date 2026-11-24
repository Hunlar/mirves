# Telegram Site Stream Bot (Heroku starter)

Telegram grup görüntülü sohbetine **yetkili, doğrudan medya URL'leri** (MP4/HLS) göndermek için başlangıç projesi.

## Gerçekçi kapsam

- BotFather botu komutları alır.
- Ayrı bir MTProto kullanıcı oturumu (`SESSION_STRING`) görüntülü sohbete yayın hesabı olarak katılır.
- `/play https://.../video.m3u8` veya doğrudan MP4 bağlantısı yayın isteği gönderir.
- `/stop`, `/sources`, `/id` komutları bulunur.
- `sources/hdfilm.py` ve `sources/puhutv.py` ayrı adaptör yuvalarıdır.

**Bu sürüm HD Film Cehennemi veya PuhuTV'den otomatik video çıkarmaz.** Bu sitelerin doğrulanmış, izinli bir API/partner akışı bulunmadığı için cookie toplama, oturum taklidi, DRM/paywall/geo-kısıt aşma veya korumalı oynatıcıdan URL çıkarma kodu eklenmedi. İlgili sağlayıcıdan yazılı izin ve resmî entegrasyon/API gelirse adaptörler tamamlanabilir.

## Gerekli Telegram bilgileri

1. `@BotFather` üzerinden yeni bot oluşturup `BOT_TOKEN` alın.
2. `my.telegram.org` üzerinden `API_ID` ve `API_HASH` alın.
3. Yayına katılacak kendi Telegram kullanıcı hesabınız için Pyrogram `SESSION_STRING` üretin. Bu değer hesap oturumudur; kimseyle paylaşmayın ve GitHub'a koymayın.
4. Yayın hesabını hedef süper gruba ekleyin.
5. Telegram uygulamasından grupta görüntülü sohbeti elle başlatın. Bu başlangıç projesi görüntülü sohbeti kendi başına başlatmaz.

## Heroku dağıtımı

Bu proje `Aptfile` ile FFmpeg, `Procfile` ile web dyno başlatır. Heroku uygulamaları Git deposundan dağıtılır; kaynak kodu önce GitHub'a yüklenmelidir.

1. ZIP'i açın ve içeriğini bir GitHub deposunun köküne yükleyin.
2. Heroku'da **New → Create new app** ile uygulama oluşturun.
3. **Deploy → GitHub → Connect to GitHub** ile depoyu bağlayın.
4. **Settings → Config Vars** bölümüne `.env.example` içindeki değerleri ekleyin.
5. **Deploy → Deploy Branch** seçin.
6. **Resources** bölümünde `web` dyno'sunu açın.
7. **Logs** bölümünden başlangıç hatalarını kontrol edin.

> Heroku'nun güncel planları ücretlidir. Bu uygulama tek `web` dyno'sunda botu ve sağlık kontrolünü birlikte çalıştırır. Heroku'nun dosya sistemi geçicidir. Uzun süreli ve yoğun video restream'i için Heroku uygun/garantili bir yayın sunucusu değildir; dyno yeniden başlatılabilir, kaynak ve ağ sınırları vardır.

## Kullanım

Hedef grupta görüntülü sohbet açıkken:

- `/start`
- `/id` — grup kimliğini öğrenin
- `/play https://izinli-host.example/video.m3u8`
- `/stop`
- `/sources`

`ALLOWED_CHAT_ID` değerini hedef grubun ID'si yapmanız önerilir.

## Güvenlik

- Bot tokeni, API hash'i ve session string'i sadece Heroku Config Vars'a girin.
- Bunları GitHub'a, sohbete veya ekran görüntüsüne koymayın.
- Session String sızarsa Telegram oturumunu sonlandırın.
- Yalnızca yayınlama ve yeniden iletme hakkınız olan içerikleri kullanın.

## Sınırlamalar / notlar

- PyTgCalls, MTProto kullanıcı istemcisi ve Telegram API bilgileri gerektirir.
- Grup görüntülü sohbeti önceden açık olmalıdır.
- Hedef medya sunucusu Heroku'dan erişilebilir olmalıdır.
- Bu başlangıç sürümü URL tabanlıdır; site kataloğu araması, bölüm listesi veya otomatik site oynatıcı çözümlemesi içermez.
- `py-tgcalls` sürümü veya Telegram tarafındaki değişiklikler nedeniyle ilk dağıtımda uyumluluk düzeltmesi gerekebilir.
