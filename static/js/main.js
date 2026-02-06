
/* ================= GLOBAL MAIN JS ================= */
/* Works safely on ALL pages */

document.addEventListener("DOMContentLoaded", () => {

    /* ================= NAVBAR SCROLL EFFECT ================= */
    const navbar = document.querySelector(".navbar");
    if (navbar) {
        window.addEventListener("scroll", () => {
            navbar.classList.toggle("scrolled", window.scrollY > 50);
        });
    }

    /* ================= FLASH MESSAGE AUTO HIDE ================= */
    const flashes = document.querySelectorAll(".flash, .toast");
    flashes.forEach(msg => {
        setTimeout(() => {
            msg.classList.add("hide");
        }, 4000);
    });

    /* ================= PRODUCT IMAGE HOVER ================= */
    document.querySelectorAll(".product-card img").forEach(img => {
        img.addEventListener("mouseenter", () => {
            img.style.transform = "scale(1.05)";
        });
        img.addEventListener("mouseleave", () => {
            img.style.transform = "scale(1)";
        });
    });

    /* ================= ADD TO CART LOADING ================= */
    document.querySelectorAll(".btn-primary").forEach(btn => {
        if (btn.textContent.toLowerCase().includes("add to cart")) {
            btn.addEventListener("click", () => {
                btn.disabled = true;
                btn.innerHTML = "Adding...";
            });
        }
    });

    /* ================= CART QUANTITY UPDATE ================= */
    document.querySelectorAll(".qty-input").forEach(input => {
        input.addEventListener("change", () => {
            input.closest("form")?.submit();
        });
    });

    /* ================= CHECKOUT PAYMENT TOGGLE ================= */
    const paymentRadios = document.querySelectorAll('input[name="payment_method"]');
    const jazzcashBox = document.getElementById("jazzcash-details");

    if (paymentRadios.length && jazzcashBox) {
        paymentRadios.forEach(radio => {
            radio.addEventListener("change", () => {
                jazzcashBox.classList.toggle("active", radio.value === "jazzcash");
            });
        });
    }

    /* ================= CHECKOUT SUBMIT LOADER ================= */
    const checkoutForm = document.getElementById("checkoutForm");
    if (checkoutForm) {
        checkoutForm.addEventListener("submit", () => {
            const btn = document.getElementById("placeOrderBtn");
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Processing...`;
            }
        });
    }

    /* ================= PRODUCT DETAILS IMAGE SWITCH ================= */
    const mainImage = document.querySelector(".main-product-image");
    const thumbs = document.querySelectorAll(".product-thumb");

    if (mainImage && thumbs.length) {
        thumbs.forEach(thumb => {
            thumb.addEventListener("click", () => {
                mainImage.src = thumb.src;
            });
        });
    }

    /* ================= CONTACT & SUPPORT FORM VALIDATION ================= */
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", e => {
            const required = form.querySelectorAll("[required]");
            let valid = true;

            required.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add("error");
                } else {
                    field.classList.remove("error");
                }
            });

            if (!valid) {
                e.preventDefault();
                alert("Please fill all required fields.");
            }
        });
    });

    /* ================= ADMIN DELETE CONFIRM ================= */
    document.querySelectorAll(".btn-delete").forEach(btn => {
        btn.addEventListener("click", e => {
            if (!confirm("Are you sure you want to delete this item?")) {
                e.preventDefault();
            }
        });
    });

});
    let currentSlide = 0;
        const slides = document.querySelectorAll(".slide");
        const dots = document.querySelectorAll(".dot");

        function showSlide(index) {
            slides.forEach(slide => slide.classList.remove("active"));
            dots.forEach(dot => dot.classList.remove("active"));

            slides[index].classList.add("active");
            dots[index].classList.add("active");
            currentSlide = index;
        }

        // Auto slide
        setInterval(() => {
            let next = (currentSlide + 1) % slides.length;
            showSlide(next);
        }, 4000);

        // Dot click
        dots.forEach((dot, index) => {
            dot.addEventListener("click", () => showSlide(index));
        });

        // Touch swipe (mobile)
        let startX = 0;
        document.querySelector(".slider").addEventListener("touchstart", e => {
            startX = e.touches[0].clientX;
        });

        document.querySelector(".slider").addEventListener("touchend", e => {
            let endX = e.changedTouches[0].clientX;
            if (startX - endX > 50) showSlide((currentSlide + 1) % slides.length);
            if (endX - startX > 50) showSlide((currentSlide - 1 + slides.length) % slides.length);
        });/* ================= END OF MAIN JS ================= */
