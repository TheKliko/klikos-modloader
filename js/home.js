window.onload = function onload() {
    var latest_version = document.getElementById('latest-version');
    var downloads_latest = document.getElementById('downloads-latest');
    // var downloads_total = document.getElementById('downloads-total');
    var discord_online = document.getElementById('discord-online-user-count');

    const github_api = 'https://api.github.com/repos/thekliko/klikos-modloader/releases';
    const discord_api = 'https://discord.com/api/guilds/1205938827437412422/widget.json';

    var response = request(github_api)
        .then(data => {
            var downloads = data[0]['assets'][0]['download_count'];
            var version = data[0]['tag_name'];

            downloads_latest.innerHTML = downloads;
            latest_version.innerHTML = version;
        });

    var response = request(discord_api)
        .then(data => {
            var online = data['presence_count'];

            discord_online.innerHTML = `${online} online`;
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