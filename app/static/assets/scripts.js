// Mobile menu toggle
const menuBtn = document.getElementById('menuBtn');
const mobileMenu = document.getElementById('mobileMenu');

menuBtn?.addEventListener('click', () => {
  mobileMenu.classList.toggle('hidden');
});

// Close mobile menu when click link
mobileMenu?.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => mobileMenu.classList.add('hidden'));
});

// Auto year footer
const yearSpan = document.getElementById('year');
if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
}

// --- LIGHT SIMULATOR ---
const overlay = document.getElementById('heroOverlay');
const btnWarm = document.getElementById('modeWarm');
const btnCool = document.getElementById('modeCool');
const btnOff  = document.getElementById('modeOff');

function resetOverlay() {
  if(overlay) overlay.className = 'absolute inset-0 transition-colors duration-1000'; 
}

// Mode WARM
btnWarm?.addEventListener('click', () => {
  resetOverlay();
  overlay?.classList.add('bg-gradient-to-r', 'from-yellow-900/80', 'via-yellow-700/40', 'to-transparent');
});

// Mode COOL
btnCool?.addEventListener('click', () => {
  resetOverlay();
  overlay?.classList.add('bg-gradient-to-r', 'from-cyan-900/80', 'via-cyan-700/40', 'to-transparent');
});

// Mode OFF
btnOff?.addEventListener('click', () => {
  resetOverlay();
  overlay?.classList.add('bg-gradient-to-r', 'from-brandBlack', 'via-brandBlack/85', 'to-brandBlack/10');
});


// ================= AUTO HIDE FLASH MESSAGES (POPUP STYLE) =================

document.addEventListener('DOMContentLoaded', () => {
  const flashContainer = document.getElementById('flash-messages');
  
  if (flashContainer) {
    // Ambil semua elemen pesan di dalamnya
    const messages = flashContainer.querySelectorAll('div.shadow-2xl');

    // Tahan selama 3.5 detik, baru mulai hilangkan
    setTimeout(() => {
      messages.forEach(msg => {
        // 1. Animasi CSS: Geser ke atas & Memudar
        msg.style.transition = "all 0.5s ease";
        msg.style.opacity = '0';
        msg.style.transform = 'translateY(-20px)';
      });

      // 2. Hapus elemen dari HTML setelah animasi selesai
      setTimeout(() => {
        flashContainer.remove();
      }, 500); // Waktu ini harus sama dengan durasi transition (0.5s)
      
    }, 3500); 
  }
});

// ================= TOGGLE SHOW/HIDE PASSWORD =================
    function togglePassword() {
        const input = document.getElementById('passwordInput');
        const icon = document.getElementById('eyeIcon');
        
        if (input.type === "password") {
            input.type = "text";
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash"); // Ganti icon jadi mata dicoret
        } else {
            input.type = "password";
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye"); // Kembali icon mata biasa
        }
    }