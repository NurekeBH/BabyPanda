// static/shop/js/phone_mask.js
document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('id_phone_number');
    if (!input) return;

    // Массивке форматты анықтайтын үлгі
    const format = '+7(___)___ __ __';
    input.setAttribute('placeholder', format);

    input.addEventListener('input', function (e) {
        let digits = e.target.value.replace(/\D/g, '');

        // Өзіміз +"7" қойып алған соң, бірінші цифрды қиып тастау
        if (digits.startsWith('7')) digits = digits.slice(1);

        let result = '+7(';
        if (digits.length > 0) result += digits.substring(0, 3);
        if (digits.length >= 3) result += ')';
        if (digits.length >= 3) result += digits.substring(3, 6);
        if (digits.length >= 6) result += ' ';
        if (digits.length >= 6) result += digits.substring(6, 8);
        if (digits.length >= 8) result += ' ';
        if (digits.length >= 8) result += digits.substring(8, 10);

        e.target.value = result;
    });
});
