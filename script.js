document.addEventListener("DOMContentLoaded", () => {
    /* ---------------- State ---------------- */
    const state = {
        features: ["Active noise cancelling", "40h battery life", "Memory-foam earcups"],
        keywords: ["wireless headphones", "noise cancelling"],
        tone: "Professional",
        length: 1 // 0 short, 1 medium, 2 long
    };

    const LENGTHS = [
        { label: "Short", words: "~35 words" },
        { label: "Medium", words: "~60 words" },
        { label: "Long", words: "~90 words" }
    ];

    /* ---------------- Helpers ---------------- */
    const $ = (id) => document.getElementById(id);

    const escapeHtml = (s) => {
        return String(s)
            .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
    };

    /* ---------------- Rendering ---------------- */
    const checkSvg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>';

    function renderVariations(variations) {
        const lenLabel = LENGTHS[state.length].label;
        variations.forEach((v, i) => {
            const panel = $("panel" + (i + 1));
            if (!panel) return;
            const wc = v.wordCount || 0;
            const highlightItems = v.highlights.map((h) => {
                return '<li>' + checkSvg + ' ' + escapeHtml(h) + '</li>';
            }).join("");

            panel.innerHTML =
                '<div class="result-item">' +
                  '<div class="result-top">' +
                    '<span class="badge">' + escapeHtml(v.id) + '</span>' +
                    '<span class="meta" style="font-size:12px;color:var(--muted-foreground);">' + wc + ' words</span>' +
                  '</div>' +
                  '<div class="result-body"><p data-copy-body>' + escapeHtml(v.body) + '</p></div>' +
                  '<ul class="highlights">' + highlightItems + '</ul>' +
                  '<div class="seo-box">' +
                    '<div class="seo-label">SEO Title</div>' +
                    '<div class="seo-title" data-copy-title>' + escapeHtml(v.seoTitle) + '</div>' +
                    '<div class="seo-label">Meta Description</div>' +
                    '<div class="seo-meta" data-copy-meta>' + escapeHtml(v.seoMeta) + '</div>' +
                  '</div>' +
                  '<div class="result-foot">' +
                    '<span class="meta">' + escapeHtml(state.tone) + ' tone · ' + lenLabel + ' length</span>' +
                    '<div class="foot-actions">' +
                      '<button class="btn btn-outline btn-sm" data-action="regenerate" data-index="' + i + '">Regenerate</button>' +
                      '<button class="btn btn-primary btn-sm" data-action="copy" data-index="' + i + '">Copy</button>' +
                    '</div>' +
                  '</div>' +
                '</div>';
        });
        $("resultsCount").textContent = "3 variations ready";
    }

    /* ---------------- Chips ---------------- */
    function renderChips(kind) {
        const container = kind === "feature" ? $("featureChips") : $("keywordChips");
        const input = kind === "feature" ? $("featureInput") : $("keywordInput");
        const list = kind === "feature" ? state.features : state.keywords;

        if (!container || !input) return;

        // remove existing chip spans
        Array.prototype.slice.call(container.querySelectorAll(".chip")).forEach((c) => { c.remove(); });

        list.forEach((value, idx) => {
            const span = document.createElement("span");
            span.className = "chip";
            span.innerHTML = escapeHtml(value) + ' <span class="x" role="button" aria-label="Remove ' + escapeHtml(value) + '">&times;</span>';
            span.querySelector(".x").addEventListener("click", () => {
                list.splice(idx, 1);
                renderChips(kind);
            });
            container.insertBefore(span, input);
        });
    }

    function setupChipInput(kind) {
        const input = kind === "feature" ? $("featureInput") : $("keywordInput");
        const list = kind === "feature" ? state.features : state.keywords;
        if (!input) return;

        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                const val = input.value.trim();
                if (val && list.indexOf(val) === -1) {
                    list.push(val);
                    input.value = "";
                    renderChips(kind);
                }
            } else if (e.key === "Backspace" && input.value === "" && list.length) {
                list.pop();
                renderChips(kind);
            }
        });
    }

    /* ---------------- Toast ---------------- */
    let toastTimer;
    function showToast(msg) {
        const toast = $("toast");
        if (!toast) return;
        $("toastText").textContent = msg;
        toast.classList.add("show");
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => { toast.classList.remove("show"); }, 2000);
    }

    /* ---------------- Copy ---------------- */
    function copyVariation(index, btn) {
        const panel = $("panel" + (index + 1));
        if (!panel) return;
        const body = panel.querySelector("[data-copy-body]");
        const title = panel.querySelector("[data-copy-title]");
        const meta = panel.querySelector("[data-copy-meta]");
        const text = (body ? body.textContent : "") +
          "\n\nSEO Title: " + (title ? title.textContent : "") +
          "\nMeta Description: " + (meta ? meta.textContent : "");

        const done = () => {
            showToast("Copied to clipboard");
            if (btn) {
                const original = btn.textContent;
                btn.textContent = "Copied!";
                btn.classList.add("copied");
                setTimeout(() => { btn.textContent = original; btn.classList.remove("copied"); }, 1500);
            }
        };

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(done, () => { fallbackCopy(text); done(); });
        } else {
            fallbackCopy(text);
            done();
        }
    }

    function fallbackCopy(text) {
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta);
    }

    /* ---------------- Generate flow ---------------- */
    let isGenerating = false;
    async function runGenerate() {
        if (isGenerating) return;
        isGenerating = true;

        const btn = $("generateBtn");
        const btnText = $("generateBtnText");
        const originalText = btnText.textContent;

        btn.setAttribute("disabled", "true");
        btnText.innerHTML = '<span class="spinner" style="display:inline-block;vertical-align:middle;"></span> Generating…';
        $("resultsCount").textContent = "Generating…";

        // Gather variables
        const name = $("pname").value.trim() || "This product";
        const category = $("cat").value;
        const audience = $("aud").value.trim() || "everyone";
        const featuresStr = state.features.join(",");
        const keywordsStr = state.keywords.join(",");
        
        const formData = new FormData();
        formData.append("name", name);
        formData.append("category", category);
        formData.append("audience", audience);
        formData.append("features", featuresStr);
        formData.append("keywords", keywordsStr);
        formData.append("tone", state.tone);
        formData.append("length", state.length);

        try {
            const response = await fetch("generate.php", {
                method: "POST",
                body: formData
            });
            const data = await response.json();

            if (data.success && data.variations) {
                renderVariations(data.variations);
                showToast("3 fresh descriptions generated");
            } else {
                alert(data.error || "Generation failed on the server.");
            }
        } catch (error) {
            console.error("Fetch generation error:", error);
            alert("Connection error. Ensure your local PHP server is running.");
        } finally {
            btn.removeAttribute("disabled");
            btnText.textContent = originalText;
            isGenerating = false;
        }
    }

    /* ---------------- Event wiring ---------------- */
    // Tone selection
    const toneGrid = $("toneGrid");
    if (toneGrid) {
        toneGrid.addEventListener("click", function (e) {
            const opt = e.target.closest(".tone-opt");
            if (!opt) return;
            Array.prototype.slice.call(this.querySelectorAll(".tone-opt")).forEach((o) => { o.classList.remove("active"); });
            opt.classList.add("active");
            state.tone = opt.getAttribute("data-tone");
        });
    }

    // Length slider
    const lenSlider = $("len");
    if (lenSlider) {
        lenSlider.addEventListener("input", function () {
            state.length = parseInt(this.value, 10);
            const l = LENGTHS[state.length];
            $("lenHint").textContent = "— " + l.label + " (" + l.words + ")";
        });
    }

    // Generate button
    const genBtn = $("generateBtn");
    if (genBtn) {
        genBtn.addEventListener("click", runGenerate);
    }

    // Delegated copy / regenerate on results
    const tabContent = document.querySelector(".tab-content");
    if (tabContent) {
        tabContent.addEventListener("click", (e) => {
            const btn = e.target.closest("button[data-action]");
            if (!btn) return;
            const index = parseInt(btn.getAttribute("data-index"), 10);
            const action = btn.getAttribute("data-action");
            if (action === "copy") {
                copyVariation(index, btn);
            } else if (action === "regenerate") {
                const original = btn.textContent;
                btn.textContent = "…";
                btn.setAttribute("disabled", "true");
                setTimeout(async () => {
                    await runGenerate();
                    btn.removeAttribute("disabled");
                    btn.textContent = original;
                }, 450);
            }
        });
    }

    /* ---------------- Login modal popup handler ---------------- */
    const signInBtn = document.querySelector('a.btn-ghost');
    const loginModal = document.getElementById('loginModal');
    if (signInBtn && loginModal) {
        signInBtn.addEventListener('click', (e) => {
            e.preventDefault();
            loginModal.style.display = 'flex';
        });
    }

    // Close button
    const closeBtn = document.getElementById('closeModalBtn');
    if (closeBtn && loginModal) {
        closeBtn.addEventListener('click', () => {
            loginModal.style.display = 'none';
        });
    }

    // Handle Login Form Submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            try {
                const response = await fetch('login.php', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                if (data.success) {
                    alert('Successfully Logged In!');
                    loginModal.style.display = 'none';
                    if (signInBtn) {
                        signInBtn.textContent = 'Sign Out';
                        signInBtn.href = '?logout=true';
                        signInBtn.className = 'btn btn-ghost logged-in';
                    }
                } else {
                    alert(data.message || 'Login failed.');
                }
            } catch (error) {
                console.error("Login error:", error);
                alert("Server error occurred during login.");
            }
        });
    }

    /* ---------------- Init ---------------- */
    setupChipInput("feature");
    setupChipInput("keyword");
    renderChips("feature");
    renderChips("keyword");
    runGenerate(); // Start with initial generation
});
