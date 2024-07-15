window.onload = function onload() {
    if (mobile_device()) {
        mobile_specific();
    }
    
    load_releases();
};

function hamburger_menu_toggle() {
    if (mobile_device()) {
        var nav = document.getElementById('header-navigation');
        if (nav.style.display === 'flex') {
            nav.style.display = 'none';
        } else {
            nav.style.display = 'flex';
        };

        load_releases();
    };
};

function mobile_device() {
    return window.innerWidth <= 768;
};

function mobile_specific() {
    var navigation = document.getElementById('header-navigation');
    var hamburger = document.getElementById('header-hamburger');

    hamburger.addEventListener('click', function() {
        navigation.classList.toggle('active')
        hamburger.classList.toggle('active')
    });
};

function desktop_specific() {
    // idk
};

function load_releases() {
    const github_api = 'https://api.github.com/repos/thekliko/klikos-modloader/releases';

    const section_start = '<section><div class="content">'
    const section_end = '</div></section>'

    const iframe_start_lightmode = `<iframe frameBorder=\'0\' class="darkmode-hidden" srcdoc="<html><head><link rel=\'stylesheet\' href=\'css/changelog-iframe.css\'></head><body>`;
    const iframe_start_darkmode = `<iframe frameBorder=\'0\' class="lightmode-hidden" srcdoc="<html><head><link rel=\'stylesheet\' href=\'css/changelog-iframe-darkmode.css\'></head><body>`;
    const iframe_end = '</body></html>"></iframe>';

    const button_action_start = '<a class=\'button action\' href=\'';
    const button_fill_start = '<a class=\'button action fill\' href=\'';

    var container = document.getElementById('desktop-container');

    var releases = [];
    var response = request(github_api)
        .then(data => {
            if (!data || data.length === 0) return;

            for (let item of data) {
                
                if (item.assets && item.assets.length > 0 && !item.draft && !item.prerelease) {
                    var browser_download_url = item.assets[0].browser_download_url;
                    var html_url = item.html_url;
                    var name = item.name;
                    var published_at = get_formatted_date(item.published_at);
                    var body = get_formatted_release_notes(item.body);

                    var iframe = `${iframe_start_lightmode}${body}${iframe_end}${iframe_start_darkmode}${body}${iframe_end}`;
                    var download_button = `${button_fill_start}${browser_download_url}\' target=\'_blank\'>Direct download</a>`
                    var github_button = `${button_action_start}${html_url}\' target=\'_blank\'>View on GitHub</a>`
                    
                    var release_name_date = `<div class=\'release-name-date\'>${name}<span class=\'mobile-hidden\'>|</span>${published_at}</div>`;
                    // var release_name_date_separator = `<div class=\'release-name-date-separator mobile-hidden\'>|</div>`;
                    // var release_date = `<div class=\'release-date\'>${published_at}</div>`;
                    var release_buttons = `<div class=\'release-button\'>${download_button}${github_button}</div>`;
                    var release_notes = `<div class=\'release-notes\'><p>Release notes:</p>${iframe}</div>`;

                    var release_content = `<div class=\'release\'>${release_name_date}${release_notes}${release_buttons}</div>`;

                    releases.push(release_content);
                };
            };
            container.innerHTML = `${section_start}${releases.join('')}${section_end}`;
        });
};

function request(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            };
            return response.json();
        });
};

function get_formatted_date(date_string) {  // Generated with ChatGPT
    const date = new Date(date_string);

    // Extract the date components
    const year = date.getUTCFullYear();
    const month = String(date.getUTCMonth() + 1).padStart(2, '0'); // Months are zero-based, so add 1
    const day = String(date.getUTCDate()).padStart(2, '0');

    // Extract the time components
    const hours = String(date.getUTCHours()).padStart(2, '0');
    const minutes = String(date.getUTCMinutes()).padStart(2, '0');

    // Format the components into the desired string
    return`${year}/${month}/${day} (${hours}:${minutes})`;
};

function get_formatted_release_notes(notes) {  // Generated with ChatGPT
    // Escape HTML characters
    notes = notes.replace(/&/g, '&amp;')
                 .replace(/</g, '&lt;')
                 .replace(/>/g, '&gt;')
                 .replace(/"/g, '&quot;');

    // Convert markdown-like syntax to HTML
    notes = notes
        .replace(/## (.*?)(\r\n|\n)/g, '') // Remove headings
        .replace(/^\s*-\s*(.*?)(\r\n|\n)/gm, (match, content) => {
            return content.trim() + '<br />'; // Keep content without the '-'
        })
        .replace(/^\s* {2,}-\s*(.*?)(\r\n|\n)/gm, (match, content) => {
            return '    ' + content.trim() + '<br />'; // Indent for sub-items
        })
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Preserve bold formatting
        .replace(/\*(.*?)\*/g, '<em>$1</em>'); // Preserve italic formatting

    // Replace line breaks with <br>
    notes = notes.replace(/(\r\n|\n)/g, '<br />');

    // Trim final output to avoid extra breaks
    notes = notes.replace(/(<br\s*\/?>\s*){2,}/g, '<br />').replace('<br />', '<br>');
    
    notes = notes.replace('<br />- ','');

    return notes;
}