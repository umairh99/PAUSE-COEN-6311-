const url = 'http://127.0.0.1:8000/'

const headers = {
    "Accept": '*/*',
    // 'sessionid': getCookie('sessionid')
}

const handleUpdateProfile = async (e) => {
    e.preventDefault()
    const formData = new FormData(document.getElementById('profile'))
    const location = url + 'profile/'

    const api = await fetch(location, {
        headers: headers,
        method: "PUT",
        body: formData
    })
    switch (api.status) {
        case 200:
            Toastify({
                text: "Profile updated successfully",
                duration: 3000,
                gravity: "bottom",
                position: 'left',
                backgroundColor: "#6b21a8",
                stopOnFocus: true
            }).showToast()
            setTimeout(() => {
                window.location.reload()
            }, 500);
            break;

        case 403:
            const apiRes = await api.json()
            console.log(apiRes)
            break

        default:

            break;
    }
}

const handleUpdatePassword = async (e) => {
    e.preventDefault()
    const formData = new FormData(document.getElementById('profile'))
    const location = url + 'security/'

    const api = await fetch(location, {
        headers: headers,
        method: "PUT",
        body: formData
    })
    switch (api.status) {
        case 200:
            Toastify({
                text: "Password updated successfully",
                duration: 3000,
                gravity: "bottom",
                position: 'left',
                backgroundColor: "#6b21a8",
                stopOnFocus: true
            }).showToast()
            setTimeout(() => {
                window.location.href = '/login'
            }, 500);
            break;
        case 403:
            Toastify({
                text: "Invalid Current Password or new password mismatch",
                duration: 3000,
                gravity: "bottom",
                position: 'left',
                backgroundColor: "#6b21a8",
                stopOnFocus: true
            }).showToast()
            break

        default:
            break;
    }
}