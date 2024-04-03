document.addEventListener("DOMContentLoaded", function() {
    const flightFrom = document.getElementById("flightFrom");
    const hotel = document.getElementById("hotel");
    const sightseeing = document.getElementById("sightseeing");
    const hotelSelection = document.getElementById("hotelSelection");
    const sightseeingSelection = document.getElementById("sightseeingSelection");

    flightFrom.addEventListener("change", function() {
        if (flightFrom.value === "city1") {
            populateOptions(hotel, ["Hotel A1", "Hotel B1", "Hotel C1"]);
            populateOptions(sightseeing, ["Sightseeing A1", "Sightseeing B1", "Sightseeing C1"]);
        } else if (flightFrom.value === "city2") {
            populateOptions(hotel, ["Hotel A2", "Hotel B2", "Hotel C2"]);
            populateOptions(sightseeing, ["Sightseeing A2", "Sightseeing B2", "Sightseeing C2"]);
        } else if (flightFrom.value === "city3") {
            populateOptions(hotel, ["Hotel A3", "Hotel B3", "Hotel C3"]);
            populateOptions(sightseeing, ["Sightseeing A3", "Sightseeing B3", "Sightseeing C3"]);
        } else {
            hotelSelection.style.display = "none";
            sightseeingSelection.style.display = "none";
        }

        hotelSelection.style.display = "block";
    });

    function populateOptions(selectElement, options) {
        selectElement.innerHTML = ""; // Clear current options

        options.forEach(option => {
            const optionElement = document.createElement("option");
            optionElement.value = option;
            optionElement.text = option;
            selectElement.appendChild(optionElement);
        });
    }

    hotel.addEventListener("change", function() {
        if (hotel.value !== "") {
            sightseeingSelection.style.display = "block";
        } else {
            sightseeingSelection.style.display = "none";
        }
    });

    sightseeing.addEventListener("change", function() {
        if (sightseeing.value !== "") {
            alert("Package selected successfully!");
        }
    });
});