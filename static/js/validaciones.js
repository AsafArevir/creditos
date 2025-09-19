// Validaciones para el formulario de crédito
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('creditForm');

    const inputs = [
        // Validaciones de campos
        {
            input: form.querySelector('input[name="cliente"]'),
            error: document.getElementById('cliente-error'),
            validator: val => val.trim() !== '' && /^[a-zA-ZáéíóúÁÉÍÓÚüñÑ\s]{3,100}$/.test(val.trim()),
            touched: false
        },
        {
            input: form.querySelector('input[name="plazo"]'),
            error: document.getElementById('plazo-error'),
            validator: val => val.trim() !== '' && /^\d+$/.test(val.trim()),
            touched: false
        },
        {
            input: form.querySelector('input[name="monto"]'),
            error: document.getElementById('monto-error'),
            validator: val => val.trim() !== '' && /^\d+(\.\d{1,2})?$/.test(val.trim()),
            touched: false
        },
        {
            input: form.querySelector('input[name="tasa_interes"]'),
            error: document.getElementById('tasa-error'),
            validator: val => val.trim() !== '' && /^\d+(\.\d{1,2})?$/.test(val.trim()),
            touched: false
        },
        {
            input: form.querySelector('input[name="fecha_otorgamiento"]'),
            error: document.getElementById('fecha-error'),
            validator: val => val.trim() !== '',
            touched: false
        }
    ];

    function validateInput(f, forceShow = false) {
        const val = f.input.value;
        const isValid = f.validator(val);

        if (!isValid && (f.touched || forceShow)) {
            f.error.classList.add('show');
            f.input.classList.add('input-error');
        } else {
            f.error.classList.remove('show');
            f.input.classList.remove('input-error');
        }

        return isValid;
    }

    inputs.forEach(f => {
        f.input.addEventListener('input', () => {
            f.touched = true;
            validateInput(f);
        });
        f.input.addEventListener('blur', () => {
            f.touched = true;
            validateInput(f);
        });
    });

    // Validación al enviar
    form.addEventListener('submit', e => {
        let allValid = true;

        inputs.forEach(f => {
            if (!validateInput(f, true)) allValid = false;
        });

        if (!allValid) {
            e.preventDefault();
        }
    });

    // Resetear errores al cerrar modal
    window.closeModal = () => {
        inputs.forEach(f => {
            f.error.classList.remove('show');
            f.input.classList.remove('input-error');
            f.touched = false;
        });
        document.getElementById('modal').classList.add('hidden');
    };
});


