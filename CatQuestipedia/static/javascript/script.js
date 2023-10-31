const colorThemes = document.getElementsByClassName('theme');

const tags = document.getElementsByClassName("searched");

const searchBox = document.getElementsByClassName("search-input");

const previewer = document.getElementsByClassName("preview-content");

const storeTheme = function (theme) {
    localStorage.setItem("preferredTheme", theme);
};

const setTheme = function () {
    const activeTheme = localStorage.getItem("preferredTheme");
    for (let theme of colorThemes) {
        if (theme.value === activeTheme) {
            theme.checked = true;
        }};
        document.documentElement.className = activeTheme;
};

const openTab = function (tab) {
    const allTabs = document.getElementsByClassName("tab-content");
    for (let tab of allTabs) {
        tab.style.display = "none";
    };
    const tabContents = document.querySelector("[value='" + tab + "']");
    tabContents.style.display = "block";
};

const updateLvl = function() {
    const selector = document.getElementsByClassName("playthrough-selector");
    var selectorValue = selector[0].options[selector[0].selectedIndex].getAttribute("name");
    document.getElementsByClassName("equipment_level_input")[0].placeholder = selectorValue;
    if (selectorValue != 0) {
        document.getElementsByClassName("equipment_owned_input")[0].checked = true;
    } else {
        document.getElementsByClassName("equipment_owned_input")[0].checked = false;
    };
};

const updateSpellLvl = function() {
    const selector = document.getElementsByClassName("playthrough-selector");
    var selectorValue = selector[0].options[selector[0].selectedIndex].getAttribute("name");
    document.getElementsByClassName("spell_level_input")[0].placeholder = selectorValue;
    if (selectorValue != 0) {
        document.getElementsByClassName("spell_known_input")[0].checked = true;
    } else {
        document.getElementsByClassName("spell_known_input")[0].checked = false;
    };
};

const updateQuest = function() {
    const selector = document.getElementsByClassName("playthrough-selector");
    var selectorValue = selector[0].options[selector[0].selectedIndex].getAttribute("name");
    if (selectorValue != 0) {
        document.getElementsByClassName("quest-completed-input")[0].checked = true;
    } else {
        document.getElementsByClassName("quest-completed-input")[0].checked = false;
    };
};

const searched = function(value) {
    searchBox[0].value = value;
    document.search.submit();
};

const updatePreview = function(content) {
    previewer[0].innerHTML = content;
};

window.onload = function () {
    for (let theme of colorThemes) {
        theme.addEventListener("click", () => {
            storeTheme(theme.value);
            document.documentElement.className = theme.value;
        });
    };
    setTheme();
};
