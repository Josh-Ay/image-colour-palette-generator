import {customErrorDiv, customResultsDiv} from "./custom.js";
import { checkImageFile } from "./validator.js";

const uploadFile = document.getElementById("upload-img");
const imgPreviewContainer = document.querySelector(".loaded-image-preview-container");
const imgPreview = document.querySelector("img.loaded-image-preview");
const addContainer = document.querySelector(".add-image-container");
const container = document.querySelector(".container-fluid");
const detailsContainer = document.querySelector(".image-details-container");
const loading = document.getElementById("loading");
const uploadNewBtn = document.querySelector(".upload-new-link");
const aboutContainer = document.querySelector(".about-container");


// function to handle file/image drag over
window.dragOver = (element, e) =>{
    e.preventDefault(); // prevent browser's default behaviour handling the event(opening the file)
    element.classList.add("drag-over");
};

// function to handle file/image drag leave
window.dragLeave = (element) =>{
    element.classList.remove("drag-over");
};

// function to remove 'select file' display and send the uploaded image
const removeFileDisplayAndSendImage = (fileAdded) =>{
    addContainer.remove();  // remove the file upload display
    aboutContainer.remove();    // remove the about section

    let newImgSrc = URL.createObjectURL(fileAdded);     // create a new blob url
    imgPreview.src = newImgSrc;     // set the img src to the blob url

    imgPreview.onload = () => {
        imgPreviewContainer.style.display = "block";

        sendLoadedImageToServer(fileAdded);     // send the image file added to the server
        showLoadingAnimation();

        URL.revokeObjectURL(imgPreview.src);    // remove the blob object from browser memory to free up memory
    }

}

// function to handle file/image drop
window.drop = (element, e) =>{
    e.preventDefault(); // prevent browser's default behaviour handing the event(opening the file)
    element.classList.remove("drag-over");

    if (e.dataTransfer.items){
        if (e.dataTransfer.items[0].kind === "file"){   // accept only files
            if (e.dataTransfer.items.length > 1){   // handle if more than one file was dropped
                customErrorDiv("Please select only one file.", container);
            }else{
                const result = checkImageFile(e.dataTransfer.items[0].type);    // check if the filetype is one of the accepted filetypes('.jpg', '.jpeg', '.png')
                if (result){
                    removeFileDisplayAndSendImage(e.dataTransfer.items[0].getAsFile()); // load the image and send it for analysis
                }else{
                    customErrorDiv("Please select an image.", container)
                };
            };
        }else{
            customErrorDiv("Please upload a file.", container);
        };
    }
};

// function to open 'select-file' dialog
window.openFiles = () =>{
    uploadFile.click();     // opens up the 'select file' window
};


// handle image/file load into div
window.addEventListener("load", () => {
    uploadFile.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            const result = checkImageFile(e.target.files[0].type);

            if (result){
                removeFileDisplayAndSendImage(e.target.files[0]);
            }else{
                customErrorDiv("Please select an image.", container);
            }
        };
    });
});

// function to show loading animation
const showLoadingAnimation = () =>{
    loading.style.display = "block";
    loading.classList.add("display");

    let distanceFromTop = loading.offsetTop;

    window.scrollTo({
        top: distanceFromTop,
        behaviour: "smooth"
    });
}


// hide loading animation
const hideLoadingAnimation = () =>{
    loading.style.display = "none";
    loading.classList.remove("display");
}


// function to send uploaded file to server
const sendLoadedImageToServer = async (imageFileToSend) => {
    let newForm = new FormData();

    newForm.append("file", imageFileToSend)     // appending the file uploaded by the user to the form created above

    // make asynchronous post request to server
    try {
        const request = await fetch("/", {method: "POST", body: newForm});
        const response = await request.json();

        detailsContainer.style.display = "block";
        customResultsDiv(response["results"], detailsContainer);    // create results div with the results gotten back

        uploadNewBtn.style.display = "block";
        hideLoadingAnimation();     // hide loading animation

    } catch (error) {
        console.log(error);
        customErrorDiv("Something went wrong while trying to extract your colors ⚠.", container);
        
        hideLoadingAnimation();
    }

};
