const url = 'http://127.0.0.1:8000/'

const headers = {
    "Accept": '*/*',
}

const request = async (location, method, formData = null) => {
    const api = await fetch(location, {
        headers: headers,
        method: method,
        body: formData
    })
    return api
}

const showToast = (message, color = '#6b21a8') => {
    Toastify({
        text: message,
        duration: 3000,
        gravity: "bottom",
        position: 'left',
        backgroundColor: color,
        stopOnFocus: true
    }).showToast()
}

const revalidate = () => {
    setTimeout(() => {
        window.location.reload()
    }, 500);
}

const redirect = (url) => {
    window.location.href = url
}

const handleUpdateProfile = async (e) => {
    e.preventDefault()
    try {
        const formData = new FormData(document.getElementById('profile'))
        const location = url + 'account/profile/'
        const api = await request(location, 'PUT', formData)

        switch (api.status) {
            case 200:
                showToast('Profile Updated')
                revalidate()
                break
            default:
                break
        }
    } catch (error) {
        redirect('/500')
    }

}

const handleUpdatePassword = async (e) => {
    e.preventDefault()
    try {
        const formData = new FormData(document.getElementById('profile'))
        const location = url + 'account/security/'
        const api = await request(location, 'PUT', formData)
        switch (api.status) {
            case 200:
                showToast('Password Updated')
                redirect('/account/login')
                break
            case 403:
                showToast('Invalid Current Password or new password mismatch')
                break
            default:
                break;
        }
    } catch (error) {
        redirect('/500')
    }
}

const handleCreateUpdateAgency = async (e, name) => {
    e.preventDefault()
    try {
        const formData = new FormData(document.getElementById('agency'))
        const location = url + 'manage/agency/'
        const method = name ? "PUT" : "POST"
        const api = await request(location, method, formData)
        switch (api.status) {
            case 200:
                showToast('Agency updated')
                revalidate()
                break
            case 201:
                showToast('Agency created')
                revalidate()
                break
            default:
                break;
        }
    } catch (error) {
        redirect('/500')
    }
}

const handleDeleteAgency = async () => {
    try {
        const location = url + 'manage/agency/'
        const api = await request(location, 'Delete')
        switch (api.status) {
            case 204:
                showToast('Agency deleted', '#991b1b')
                redirect('/')
                break
            default:
                break;
        }
    } catch (error) {
        redirect('/500')
    }
}

const handleshowhide = () => {
    const dialog = document.getElementById('dialog')
    if (dialog.open) {
        dialog.close()
    } else {
        dialog.showModal()
    }
}

const handleCreate = async (e, loc, formId, red) => {
    e.preventDefault()
    try {
        const formData = new FormData(document.getElementById(formId))
        const location = url + loc
        const api = await request(location, 'POST', formData)
        const apiRes = await api.json()
        switch (api.status) {
            case 201:
                showToast('Create successfully')
                redirect(red ? red : `/${loc}${apiRes.id}`)
                break
            case 302:
                window.location.href = apiRes.url
            default:
                break;
        }
    } catch (error) {
        console.log(error)
    }
}

const handleUpdate = async (e, loc, formId) => {
    e.preventDefault()
    try {
        const formData = new FormData(document.getElementById(formId))
        const location = url + loc
        const api = await request(location, 'PUT', formData)
        switch (api.status) {
            case 200:
                showToast('updated successfully')
                revalidate()
                break
            default:
                break;
        }
    } catch (error) {
    }
}

const handleDelete = async (e, loc, red) => {
    e.preventDefault()
    try {
        const location = url + loc
        const api = await request(location, 'DELETE')
        switch (api.status) {
            case 204:
                showToast('Deleted successfully', '#991b1b')
                redirect(`/${red}`)
                break
            default:
                break;
        }
    } catch (error) {

    }
}

const handleUploadImage = async (e, loc, formId) => {
    e.preventDefault()
    try {
        const location = url + loc
        const formData = new FormData(document.getElementById(formId))
        const api = await request(location, 'POST', formData)
        switch (api.status) {
            case 200:
                showToast('Upload successfully')
                revalidate()
                break
            default:
                break;
        }
    } catch (error) {

    }
}

const handlePopover = () => {
    popover = document.getElementById('popover')
    popover.style.display = popover.style.display == 'none' || popover.style.display == '' ? 'block' : 'none'
}


const handleAddPackage = async (e) => {
    e.preventDefault()
    try {
        const formData = new FormData(document.getElementById('addp'))
        const location = url + 'my-packages/'
        const api = await request(location, 'POST', formData)
        switch (api.status) {
            case 201:
                showToast('Added to my-packages')
                break
            case 208:
                const apiRes = await api.json()
                const locationU = url + `my-packages/${apiRes.id}/`
                const apiU = await request(locationU, 'PATCH', formData)
                switch (apiU.status) {
                    case 200:
                        showToast('Added to my-packages')
                        break
                    default:
                        break;
                }
                break
            default:
                break;
        }
    } catch (error) {
        redirect('/500')
    }
}

const handleSearch = async (e) => {
    e.preventDefault()
    const formData = new FormData(document.getElementById('sf'))
    const cover = document.getElementById('search')
    if (formData.get('search')) {
        cover.classList.add('absolute')
        cover.classList.remove('hidden')
        const location = url + `search/?search=${formData.get('search')}`
        const api = await request(location, 'GET')
        const apiRes = await api.json()
        var flightsContainer = document.getElementById('flights');
        var hotelsContainer = document.getElementById('hotels');
        var activitiesContainer = document.getElementById('activities');

        // Clear previous results
        flightsContainer.innerHTML = '';
        hotelsContainer.innerHTML = '';
        activitiesContainer.innerHTML = '';

        // Display flights
        apiRes.flights.forEach(function (flight) {
            var flightElement = document.createElement('a')
            flightElement.href = '/flights/' + flight.id
            flightElement.textContent = flight.airline; // You can replace this with the desired flight information
            flightsContainer.appendChild(flightElement);
        });

        // Display hotels
        apiRes.hotels.forEach(function (hotel) {
            var hotelElement = document.createElement('a')
            hotelElement.href = '/hotels/' + hotel.id
            hotelElement.textContent = hotel.name; // You can replace this with the desired hotel information
            hotelsContainer.appendChild(hotelElement);
        });

        // Display activities
        apiRes.activities.forEach(function (activity) {
            var activityElement = document.createElement('a')
            activityElement.href = '/activities/' + activity.id
            activityElement.textContent = activity.name; // You can replace this with the desired activity information
            activitiesContainer.appendChild(activityElement);
        })
    } else {
        cover.classList.add('hidden')
        cover.classList.remove('absolute')
    }
} 