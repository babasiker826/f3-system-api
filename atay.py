# app.py
from flask import Flask, send_from_directory, render_template_string, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import time

app = Flask(__name__)

# Rate limit konfigürasyonu
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["40 per 60 seconds", "8 per 40 seconds"]  # 40 saniyede 8 istek
)

BASE = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS = os.path.join(BASE, "downloads")

APIS = [
    ("Vergi Sorgu", "https://vergidata-hv43.onrender.com/f3system/api/vergi?vergi_no=11338465102"),
    ("Seri No", "https://serinodataf3.onrender.com/serino?tc=31702753468"),
    ("Eczane", "https://eczanedataf3.onrender.com/f3system/api/eczane?il="),
    ("Papara No", "https://paparadataf3.onrender.com/f3system/api/papara?paparano=1977050442"),
    ("Papara Ad Soyad", "https://paparadataf3.onrender.com/f3system/api/papara?ad=UFUK&soyad=DEMİR"),
    ("Plaka (TC)", "https://plakaf3.onrender.com/f3/api/plaka?tc="),
    ("Plaka (Ad Soyad)", "https://plakaf3.onrender.com/f3/api/adsoyadplaka?ad=&soyad="),
    ("Ad Soyad", "http://45.81.113.22:4040/adsoyad?ad=<AD>&soyad=<SOYAD>"),
    ("TC", "http://45.81.113.22:4040/tc?tc=<TC_NUMARASI>"),
    ("Aile", "http://45.81.113.22:4040/aile?tc=<TC_NUMARASI>"),
    ("Çocuk", "http://45.81.113.22:4040/cocuk?tc="),
    ("Anne", "http://45.81.113.22:4040/anne?tc="),
    ("Baba", "http://45.81.113.22:4040/baba?tc="),
    ("TC Pro", "http://45.81.113.22:4000/f3system/api/tcpro?tc=<TC_NO>&key=F3-TEST-KEY-123"),
    ("Adres", "http://45.81.113.22:4000/f3system/api/adres?tc=<TC_NO>&key=F3-TEST-KEY-123"),
    ("Hane", "http://45.81.113.22:4000/f3system/api/hane?tc=<TC_NO>&key=F3-TEST-KEY-123"),
    ("Sülale", "http://45.81.113.22:4000/f3system/api/sulale?tc=<TC_NO>&key=F3-TEST-KEY-123"),
    ("Aile (Key)", "http://45.81.113.22:4000/f3system/api/aile?tc=<TC_NO>&key=F3-TEST-KEY-123"),
]

@app.route("/")
@limiter.limit("40 per 60 seconds")  # Ana sayfa için de limit
def index():
    return render_template_string("""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>F3 • SON DURAK</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;500&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0a0a;--surface:#111111;--surface-light:#1a1a1a;--text:#e8e8e8;--text-muted:#888888;--accent:#c92c2c;--accent-dark:#8b1a1a;--accent-glow:rgba(201,44,44,0.15);--border:rgba(255,255,255,0.05);--success:#2ecc71}
*{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',sans-serif}
html,body{height:100%;background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased}
.bg-animation{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;background:radial-gradient(ellipse at 20% 20%, var(--accent-glow) 0%, transparent 40%),radial-gradient(ellipse at 80% 80%, rgba(20,20,30,0.3) 0%, transparent 40%),linear-gradient(180deg,#0a0a0a 0%,#050505 100%);animation:pulse 20s infinite alternate}
@keyframes pulse{0%{opacity:0.5}100%{opacity:1}}
.container{max-width:1400px;margin:0 auto;padding:30px;min-height:100vh;display:flex;flex-direction:column}
.header{text-align:center;padding:40px 0;border-bottom:1px solid var(--border);margin-bottom:40px;position:relative}
.header h1{font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:500;letter-spacing:1px;margin-bottom:10px;background:linear-gradient(90deg,#fff,var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent;display:inline-block}
.header h1::after{content:'';position:absolute;bottom:-10px;left:50%;transform:translateX(-50%);width:100px;height:2px;background:var(--accent)}
.subtitle{font-size:1.1rem;color:var(--text-muted);font-weight:300;letter-spacing:2px;text-transform:uppercase;margin-top:20px}
.quote{font-family:'JetBrains Mono',monospace;font-size:0.9rem;color:var(--accent);margin-top:30px;font-style:italic;max-width:600px;margin-left:auto;margin-right:auto;line-height:1.6;border-left:2px solid var(--accent);padding-left:15px}
.api-container{flex:1}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:25px;margin-bottom:50px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:25px;transition:all 0.3s ease;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,var(--accent),transparent)}
.card h3{font-size:1.3rem;font-weight:600;margin-bottom:10px;color:#fff}
.meta{font-size:0.85rem;color:var(--text-muted);margin-bottom:20px}
.actions{display:flex;gap:10px;margin-top:15px}
.btn{padding:10px 20px;border-radius:8px;border:none;cursor:pointer;font-weight:500;font-size:0.9rem;transition:all 0.2s ease;flex:1;text-align:center}
.btn-copy{background:var(--surface-light);color:var(--text);border:1px solid var(--border)}
.btn-open{background:linear-gradient(90deg,var(--accent-dark),var(--accent));color:white}
.search-container{max-width:500px;margin:0 auto 40px;position:relative}
.search-box{width:100%;padding:15px 20px;background:var(--surface);border:1px solid var(--border);border-radius:10px;color:var(--text);font-size:1rem}
.footer{text-align:center;padding:40px 0;border-top:1px solid var(--border);margin-top:auto;color:var(--text-muted);font-size:0.9rem}
.player-container{position:fixed;bottom:20px;right:20px;background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px 18px;display:flex;align-items:center;gap:10px;box-shadow:0 5px 20px rgba(0,0,0,0.3);z-index:1000;min-width:180px;opacity:0.9}
.player-btn{width:32px;height:32px;border-radius:50%;background:var(--accent);border:none;color:white;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0}
.player-info{flex:1;min-width:0}
#songTitle{font-size:0.8rem;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#timeDisplay{font-size:0.7rem;color:var(--text-muted);font-family:'JetBrains Mono',monospace}
.volume-slider{width:60px;height:4px;background:var(--surface-light);border-radius:2px;cursor:pointer;flex-shrink:0}
.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,5,5,0.95);display:flex;align-items:center;justify-content:center;z-index:9999}
.modal-content{background:var(--surface);border-radius:15px;padding:40px;max-width:500px;width:90%;text-align:center;border:1px solid var(--border);box-shadow:0 20px 60px rgba(0,0,0,0.7)}
.modal-title{font-family:'Playfair Display',serif;font-size:2.5rem;margin-bottom:20px;color:var(--accent)}
.modal-text{color:var(--text-muted);line-height:1.6;margin-bottom:30px;font-size:1.1rem}
.modal-btn{background:linear-gradient(90deg,var(--accent-dark),var(--accent));color:white;border:none;padding:15px 40px;border-radius:50px;font-size:1.1rem;font-weight:600;cursor:pointer}
@media (max-width:768px){.container{padding:20px}.header h1{font-size:2.5rem}.grid{grid-template-columns:1fr}.player-container{bottom:15px;right:15px;left:15px;padding:10px 15px}.player-btn{width:28px;height:28px}.volume-slider{width:50px}}
.fade-in{animation:fadeIn .8s ease forwards}@keyframes fadeIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
</style>
</head>
<body>
    <div class="bg-animation"></div>
    <div id="welcomeModal" class="modal-overlay">
        <div class="modal-content fade-in">
            <h2 class="modal-title">F3 • SON DURAK</h2>
            <div class="modal-text">
                <p>Her yolculuğun bir sonu vardır...</p>
                <p>Bu, bizim son durağımız. Tüm API'ler burada toplandı.</p>
                <p>Müzik ilk 15 saniyeyi atlayarak hemen başlayacak. Hazır mısın?</p>
            </div>
            <button class="modal-btn" onclick="startJourney()">YOLCULUĞA BAŞLA</button>
        </div>
    </div>
    <div class="container">
        <div class="header">
            <h1>F3 • SON DURAK</h1>
            <div class="subtitle">Sanaldan Gerçeğe Son Yolculuk</div>
            <div class="quote">"Bazı şeyler biter ki yenileri başlayabilsin. Bu son değil, yeni bir başlangıç."</div>
        </div>
        <div class="search-container">
            <input type="text" class="search-box" id="searchInput" placeholder="API ara... (Vergi, TC, Plaka, Papara)">
        </div>
        <div class="api-container">
            <div class="grid" id="apiGrid">
                {% for name, url in apis %}
                <div class="card fade-in" data-name="{{ name }}" data-url="{{ url }}">
                    <h3>{{ name }}</h3>
                    <div class="meta">Gizli API endpoint'i - kopyala veya yeni sekmede aç</div>
                    <div class="actions">
                        <button class="btn btn-copy" onclick="copyApi('{{ url }}', this)">📋 Kopyala</button>
                        <button class="btn btn-open" onclick="openApi('{{ url }}')">🔗 Aç</button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        <div class="footer">
            <p>© 2024 F3 SYSTEM • Tüm hakları saklıdır.</p>
            <p>Bu, sanal dünyadaki son duraktır. Gerçek hayatta görüşmek üzere...</p>
            <div class="final-message">"Gittiğin yolda güneş hep arkandan gelsin."</div>
        </div>
    </div>
    <div class="player-container" id="player" style="display: none;">
        <button class="player-btn" id="playBtn">▶</button>
        <div class="player-info">
            <div id="songTitle">piskoloji.mp3</div>
            <div id="timeDisplay">00:00 / 00:00</div>
        </div>
        <input type="range" class="volume-slider" id="volumeSlider" min="0" max="1" step="0.01" value="0.7">
        <button class="player-btn" id="muteBtn">🔊</button>
    </div>
    <audio id="bgMusic" preload="metadata">
        <source src="/muzik" type="audio/mpeg">
    </audio>
    <script>
        // Elements
        const welcomeModal = document.getElementById('welcomeModal');
        const player = document.getElementById('player');
        const bgMusic = document.getElementById('bgMusic');
        const playBtn = document.getElementById('playBtn');
        const muteBtn = document.getElementById('muteBtn');
        const volumeSlider = document.getElementById('volumeSlider');
        const timeDisplay = document.getElementById('timeDisplay');
        const searchInput = document.getElementById('searchInput');
        const apiCards = document.querySelectorAll('.card');

        // Start journey function (GÜNCELLENDİ: artık 15s atlar ve küçük müzik kutusu)
        function startJourney() {
            // Hide modal
            welcomeModal.style.opacity = '0';
            welcomeModal.style.transition = 'opacity 0.5s ease';
            setTimeout(() => { welcomeModal.style.display = 'none'; }, 500);

            // Show player (küçültülmüş versiyon)
            player.style.display = 'flex';
            player.style.opacity = '0';
            player.style.transform = 'translateY(20px)';
            setTimeout(() => {
                player.style.transition = 'all 0.5s ease';
                player.style.opacity = '0.9';
                player.style.transform = 'translateY(0)';
            }, 100);

            // Immediately attempt to seek to 15s and play
            function playFrom15() {
                try {
                    if (bgMusic.readyState >= 2) {
                        try { bgMusic.currentTime = 15; } catch (e) { console.log("Couldn't set time") }
                        bgMusic.volume = volumeSlider.value;
                        bgMusic.play().then(() => { 
                            playBtn.textContent = "❚❚"; 
                        }).catch(() => { 
                            playBtn.textContent = "▶"; 
                        });
                    } else {
                        bgMusic.addEventListener('loadedmetadata', function onMeta() {
                            try { bgMusic.currentTime = 15; } catch (e) { console.log("Couldn't set time") }
                            bgMusic.volume = volumeSlider.value;
                            bgMusic.play().then(() => { 
                                playBtn.textContent = "❚❚"; 
                            }).catch(() => { 
                                playBtn.textContent = "▶"; 
                            });
                            bgMusic.removeEventListener('loadedmetadata', onMeta);
                        }, { once: true });

                        bgMusic.play().then(() => {
                            try { bgMusic.currentTime = 15; } catch (e) { console.log("Couldn't set time") }
                            playBtn.textContent = "❚❚";
                        }).catch(() => {
                            playBtn.textContent = "▶";
                        });
                    }
                } catch (err) {
                    console.log("Fallback play");
                    bgMusic.play().catch(() => { });
                }
            }
            playFrom15();

            // notify
            showNotification("🎵 Müzik başlatıldı (15s atlandı).", "success");
        }

        // Copy API URL
        function copyApi(url, button) {
            navigator.clipboard.writeText(url).then(() => {
                const originalText = button.textContent;
                button.textContent = "✓ Kopyalandı";
                button.style.background = "var(--success)";
                button.style.color = "white";
                setTimeout(() => {
                    button.textContent = originalText;
                    button.style.background = "";
                    button.style.color = "";
                }, 2000);
            }).catch(err => {
                console.error('Copy failed:', err);
                showNotification("Kopyalama başarısız", "error");
            });
        }

        // Open API URL
        function openApi(url) {
            window.open(url, '_blank');
        }

        // Player controls
        playBtn.addEventListener('click', () => {
            if (bgMusic.paused) {
                bgMusic.play();
                playBtn.textContent = "❚❚";
            } else {
                bgMusic.pause();
                playBtn.textContent = "▶";
            }
        });

        muteBtn.addEventListener('click', () => {
            bgMusic.muted = !bgMusic.muted;
            muteBtn.textContent = bgMusic.muted ? "🔇" : "🔊";
        });

        volumeSlider.addEventListener('input', () => {
            bgMusic.volume = volumeSlider.value;
        });

        // Update time display
        bgMusic.addEventListener('timeupdate', () => {
            const current = formatTime(bgMusic.currentTime);
            const duration = formatTime(bgMusic.duration || 0);
            timeDisplay.textContent = `${current} / ${duration}`;
        });

        function formatTime(seconds) {
            if (isNaN(seconds)) return "00:00";
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }

        // Search
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            apiCards.forEach(card => {
                const name = card.getAttribute('data-name').toLowerCase();
                const url = card.getAttribute('data-url').toLowerCase();
                if (name.includes(searchTerm) || url.includes(searchTerm)) {
                    card.style.display = 'block';
                    setTimeout(() => { card.style.opacity = '1'; card.style.transform = 'translateY(0)'; }, 10);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(10px)';
                    setTimeout(() => { card.style.display = 'none'; }, 300);
                }
            });
        });

        // Notifications
        function showNotification(message, type = "info") {
            const notification = document.createElement('div');
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${type === 'success' ? 'var(--success)' : 'var(--accent)'};
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                z-index: 10000;
                animation: slideIn 0.3s ease;
            `;
            document.body.appendChild(notification);
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => { document.body.removeChild(notification); }, 300);
            }, 3000);
        }

        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
            @keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }
        `;
        document.head.appendChild(style);

        document.addEventListener('DOMContentLoaded', () => {
            apiCards.forEach((card, index) => { card.style.animationDelay = `${index * 0.05}s`; });
        });
    </script>
</body>
</html>""", apis=APIS)

@app.route("/muzik")
@limiter.limit("40 per 60 seconds")  # Müzik endpoint'i için de limit
def muzik():
    # Müzik dosyasını downloads klasöründen servis et
    return send_from_directory(DOWNLOADS, "piskoloji.mp3", mimetype="audio/mpeg")

# Rate limit aşıldığında gösterilecek özel hata sayfası
@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rate Limit Aşıldı</title>
        <style>
            body {
                background: #0a0a0a;
                color: #e8e8e8;
                font-family: 'Inter', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .error-container {
                text-align: center;
                padding: 40px;
                border: 1px solid #c92c2c;
                border-radius: 12px;
                background: #111111;
                max-width: 500px;
            }
            h1 {
                color: #c92c2c;
                font-size: 2.5rem;
                margin-bottom: 20px;
            }
            p {
                margin-bottom: 10px;
                line-height: 1.6;
            }
            .countdown {
                font-size: 1.2rem;
                color: #888888;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>⏱️ Rate Limit Aşıldı</h1>
            <p>40 saniye içinde maksimum 8 istek gönderebilirsiniz.</p>
            <p>Lütfen biraz bekleyip tekrar deneyin.</p>
            <p>Bu limit, sistemin stabil çalışması için konulmuştur.</p>
            <div class="countdown" id="countdown">40 saniye sonra tekrar deneyebilirsiniz</div>
        </div>
        <script>
            let seconds = 40;
            const countdownElement = document.getElementById('countdown');
            const timer = setInterval(() => {
                seconds--;
                countdownElement.textContent = seconds + " saniye sonra tekrar deneyebilirsiniz";
                if (seconds <= 0) {
                    clearInterval(timer);
                    countdownElement.textContent = "Artık tekrar deneyebilirsiniz!";
                }
            }, 1000);
        </script>
    </body>
    </html>
    """), 429

if __name__ == "__main__":
    if not os.path.isdir(DOWNLOADS):
        os.makedirs(DOWNLOADS)
        print("⚠️ Lütfen 'piskoloji.mp3' dosyasını 'downloads' klasörüne yerleştirin!")
    
    print("🚀 F3 - Son Durak başlatılıyor...")
    print("🌐 Site: http://localhost:4000")
    print("⏱️ Rate Limit Aktif: 40 saniyede 8 istek")
    print("🎵 Müzik, 'YOLCULUĞA BAŞLA' tuşuna basınca hemen başlayacak (ilk 15s atlanır).")
    print("🔉 Müzik kutusu küçültüldü ve minimalist hale getirildi.")
    print("💔 Hüzünlü veda teması aktif...")
    
    app.run(host="0.0.0.0", port=4000, debug=True)
