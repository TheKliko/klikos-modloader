const socialProofStrings = [
    "{X} happy users",
    "Used by {X} modders",
    "Trusted by {X} users",
    "{X} users",
    "{X} downloads",
    "{X} downloads - Thank you ❤️",
    "Join {X} users today!",
    "{X} awesome users – Thank you!"
];


window.onload = function () {
    var span = document.getElementById("hero-social-proof");

    if (span) {
        try {
            getDownloadCount().then(downloads => {
                const randomMessage = socialProofStrings[Math.floor(Math.random() * socialProofStrings.length)];
                span.innerHTML = randomMessage.replace("{X}", downloads);
                // span.innerHTML = `${downloads} happy users`;
            });
        } catch (error) {
            console.error("Error fetching download count:", error);
        }
    }
}


async function getDownloadCount() {
    var endpoint = "https://api.github.com/repos/thekliko/klikos-modloader/releases/latest";
    let response = await fetch(endpoint);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    let data = await response.json();
    let downloads = data.assets.reduce((sum, asset) => sum + asset.download_count, 0);
    return downloads
}