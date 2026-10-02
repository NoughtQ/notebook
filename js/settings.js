(function () {
  const STORAGE_KEY = "notebook.sidebarMode";
  const LEGACY_STORAGE_KEY = "notebook.layoutMode";
  const MODES = ["auto", "fixed", "hidden"];
  const DEFAULT_MODE = "auto";
  const ROOT_ID = "notebookSettings";
  const TOGGLE_ID = "notebookSettingsToggle";
  const SIDEBAR_BUTTON_ID = "notebookSidebarModeButton";

  const modeLabels = {
    auto: "自动隐藏",
    fixed: "固定显示",
    hidden: "隐藏",
  };

  const modeIcons = {
    auto: "panel-left-dashed",
    fixed: "panel-left",
    hidden: "panel-left-close",
  };

  function isValidMode(mode) {
    return MODES.includes(mode);
  }

  function readStorage(key) {
    try {
      return localStorage.getItem(key);
    } catch (error) {
      return null;
    }
  }

  function writeStorage(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (error) {
      // Browsers may block storage in private or embedded contexts.
    }
  }

  function readStoredMode() {
    const storedMode = readStorage(STORAGE_KEY);
    if (isValidMode(storedMode)) return storedMode;

    const legacyMode = readStorage(LEGACY_STORAGE_KEY);
    return isValidMode(legacyMode) ? legacyMode : DEFAULT_MODE;
  }

  function getNextMode(mode) {
    const currentIndex = MODES.indexOf(mode);
    return MODES[(currentIndex + 1) % MODES.length] || DEFAULT_MODE;
  }

  function renderLucideIcons() {
    if (window.lucide && typeof window.lucide.createIcons === "function") {
      window.lucide.createIcons({
        attrs: {
          "aria-hidden": "true",
        },
      });
    }
  }

  function isHomePage() {
    if (document.querySelector(".md-content .homepage")) return true;

    const editLink = document.querySelector('a[rel="edit"][href*="/docs/index.md"]');
    return Boolean(editLink);
  }

  function setOpen(isOpen) {
    const root = document.getElementById(ROOT_ID);
    const toggle = document.getElementById(TOGGLE_ID);
    if (!root || !toggle) return;

    root.classList.toggle("is-open", isOpen);
    toggle.setAttribute("aria-expanded", String(isOpen));
  }

  function updateSidebarButton(mode) {
    const button = document.getElementById(SIDEBAR_BUTTON_ID);
    if (!button) return;

    const nextMode = getNextMode(mode);
    const tooltip = `侧栏：${modeLabels[mode]}。点击切换为：${modeLabels[nextMode]}`;

    button.dataset.mode = mode;
    button.setAttribute("data-tooltip", tooltip);
    button.setAttribute("aria-label", tooltip);
    button.setAttribute("title", tooltip);
    button.innerHTML = `<i data-lucide="${modeIcons[mode]}"></i>`;
    renderLucideIcons();
  }

  function applySidebarMode(mode) {
    const nextMode = isValidMode(mode) ? mode : DEFAULT_MODE;
    document.body.dataset.sidebarMode = nextMode;
    delete document.body.dataset.layoutMode;
    updateSidebarButton(nextMode);
  }

  function createSettings() {
    if (document.getElementById(ROOT_ID)) return;

    const root = document.createElement("div");
    root.id = ROOT_ID;
    root.className = "notebook-settings";
    root.innerHTML = `
      <div class="notebook-settings__options" aria-label="页面设置选项">
        <button
          class="notebook-settings__option"
          id="${SIDEBAR_BUTTON_ID}"
          type="button"
        ></button>
      </div>
      <button
        class="notebook-settings__button"
        id="${TOGGLE_ID}"
        type="button"
        aria-label="设置"
        data-tooltip="设置"
        title="设置"
        aria-expanded="false"
      ><i data-lucide="settings"></i></button>
    `;

    document.body.appendChild(root);

    const toggle = document.getElementById(TOGGLE_ID);
    const sidebarButton = document.getElementById(SIDEBAR_BUTTON_ID);

    toggle.addEventListener("click", (event) => {
      event.stopPropagation();
      setOpen(!root.classList.contains("is-open"));
    });

    sidebarButton.addEventListener("click", (event) => {
      event.stopPropagation();
      const currentMode = document.body.dataset.sidebarMode || DEFAULT_MODE;
      const nextMode = getNextMode(currentMode);
      applySidebarMode(nextMode);
      writeStorage(STORAGE_KEY, nextMode);
    });

    root.addEventListener("click", (event) => {
      event.stopPropagation();
    });

    document.addEventListener("click", () => setOpen(false));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        setOpen(false);
      }
    });
  }

  function init() {
    if (isHomePage()) return;

    createSettings();
    applySidebarMode(readStoredMode());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
