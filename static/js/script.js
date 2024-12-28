document.addEventListener("DOMContentLoaded", function() {
    // Ambil elemen-elemen dari DOM
    const form = document.getElementById('simulasiForm');
    const kasusAwalInput = document.getElementById('kasus_awal');
    const pertumbuhanMinInput = document.getElementById('pertumbuhan_min');
    const pertumbuhanMaxInput = document.getElementById('pertumbuhan_max');
    const errorMessage = document.getElementById('error-message');
    
    // Fungsi untuk validasi input
    function validateForm() {
        let valid = true;

        // Cek apakah input kosong
        if (kasusAwalInput.value === '' || pertumbuhanMinInput.value === '' || pertumbuhanMaxInput.value === '') {
            errorMessage.textContent = "Semua kolom harus diisi!";
            valid = false;
        } else {
            // Pastikan nilai adalah angka yang valid
            if (isNaN(kasusAwalInput.value) || isNaN(pertumbuhanMinInput.value) || isNaN(pertumbuhanMaxInput.value)) {
                errorMessage.textContent = "Harap masukkan nilai numerik yang valid.";
                valid = false;
            } else if (parseFloat(pertumbuhanMinInput.value) >= parseFloat(pertumbuhanMaxInput.value)) {
                errorMessage.textContent = "Pertumbuhan Min harus lebih kecil dari Pertumbuhan Max!";
                valid = false;
            } else {
                errorMessage.textContent = ''; // Reset pesan error jika valid
            }
        }

        return valid;
    }

    // Event listener untuk saat pengguna submit formulir
    form.addEventListener('submit', function(event) {
        if (!validateForm()) {
            event.preventDefault(); // Jangan kirim formulir jika tidak valid
        }
    });

    // Menyembunyikan pesan error saat pengguna mulai mengetik
    kasusAwalInput.addEventListener('input', function() {
        errorMessage.textContent = '';
    });
    pertumbuhanMinInput.addEventListener('input', function() {
        errorMessage.textContent = '';
    });
    pertumbuhanMaxInput.addEventListener('input', function() {
        errorMessage.textContent = '';
    });
});
