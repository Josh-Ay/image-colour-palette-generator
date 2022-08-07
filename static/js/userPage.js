const profileContainer = document.getElementById("user-profile-details-container");
const userPageContainer = document.querySelector(".user-profile-page-container");
const header = document.querySelector("header");
const datesContainer = document.querySelectorAll(".view-results-container .results p");


window.toggleUserProfileDiv = () => {

    if ((profileContainer.style.display === "") || (profileContainer.style.display === "none")) return profileContainer.style.display = "block";
    
    profileContainer.style.display = "none";
    
}

window.handleViewMoreBtnClick = () => {

    userPageContainer.childNodes.forEach(childNode => {

        if (childNode.style === undefined) return childNode.textContent = "";

        if (childNode.id === "go-back-btn") return childNode.style.display = "block";

        if (childNode.id === "all-user-colors-container") return childNode.style.display = "flex";

        childNode.style.display = "none";
    })

    header.classList.remove("rel-position");
    userPageContainer.classList.add("all-colors-active");

}

window.handleViewResultsBtnClick = () => {
    userPageContainer.childNodes.forEach(childNode => {

        if (childNode.style === undefined) return childNode.textContent = "";

        if (childNode.id === "go-back-btn") return childNode.style.display = "block";

        if (childNode.id === "all-results-title") return childNode.style.display = "block";

        if (childNode.id === "view-results-container") return childNode.style.display = "flex";

        childNode.style.display = "none";
    })

    header.classList.remove("rel-position");
    userPageContainer.classList.add("all-colors-active");

}

datesContainer.forEach(elem => {
    if ( new Date(elem.textContent) == "Invalid Date" ) return "";

    const daysEndingWithSt = [1, 21, 31];
    const daysEndingWithNd = [2, 22];
    const daysEndingWithRd = [3, 23];

    const dateInValidFormat = new Date(elem.textContent);

    const day = dateInValidFormat.toLocaleDateString("en-us", {day: "numeric"})
    const dayAsNumber = Number(day);
    const month = dateInValidFormat.toLocaleDateString("en-us", {month: "long"})

    if ( daysEndingWithSt.includes(dayAsNumber) ) return elem.textContent = `${day}st ${month}, ${dateInValidFormat.getFullYear()} at ${dateInValidFormat.getHours() >= 10 ? dateInValidFormat.getHours(): '0' + dateInValidFormat.getHours()}:${dateInValidFormat.getMinutes() >= 10 ? dateInValidFormat.getMinutes() : '0' + dateInValidFormat.getMinutes()}:${dateInValidFormat.getSeconds() >= 10 ? dateInValidFormat.getSeconds() : '0' + dateInValidFormat.getSeconds()}`;
    
    if ( daysEndingWithNd.includes(dayAsNumber) ) return elem.textContent = `${day}nd ${month}, ${dateInValidFormat.getFullYear()} at ${dateInValidFormat.getHours() >= 10 ? dateInValidFormat.getHours(): '0' + dateInValidFormat.getHours()}:${dateInValidFormat.getMinutes() >= 10 ? dateInValidFormat.getMinutes() : '0' + dateInValidFormat.getMinutes()}:${dateInValidFormat.getSeconds() >= 10 ? dateInValidFormat.getSeconds() : '0' + dateInValidFormat.getSeconds()}`;

    if ( daysEndingWithRd.includes(dayAsNumber) ) return elem.textContent = `${day}rd ${month}, ${dateInValidFormat.getFullYear()} at ${dateInValidFormat.getHours() >= 10 ? dateInValidFormat.getHours(): '0' + dateInValidFormat.getHours()}:${dateInValidFormat.getMinutes() >= 10 ? dateInValidFormat.getMinutes() : '0' + dateInValidFormat.getMinutes()}:${dateInValidFormat.getSeconds() >= 10 ? dateInValidFormat.getSeconds() : '0' + dateInValidFormat.getSeconds()}`;

    return elem.textContent = `${day}th ${month}, ${dateInValidFormat.getFullYear()} at ${dateInValidFormat.getHours() >= 10 ? dateInValidFormat.getHours(): '0' + dateInValidFormat.getHours()}:${dateInValidFormat.getMinutes() >= 10 ? dateInValidFormat.getMinutes() : '0' + dateInValidFormat.getMinutes()}:${dateInValidFormat.getSeconds() >= 10 ? dateInValidFormat.getSeconds() : '0' + dateInValidFormat.getSeconds()}`;

})
