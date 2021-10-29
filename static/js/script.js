import {customErrorDiv, customResultsDiv} from "./custom.js";

const uploadFile = document.getElementById("upload-img");
const imgPreviewContainer = document.querySelector(".loaded-image-preview-container");
const imgPreview = document.querySelector("img.loaded-image-preview");
const addContainer = document.querySelector(".add-image-container");
const container = document.querySelector(".container-fluid");
const detailsContainer = document.querySelector(".image-details-container");
const loading = document.getElementById("loading");
const uploadNewBtn = document.querySelector(".upload-new-link");


// function to handle file/image drag over
window.dragOver = (element, e) =>{
    e.preventDefault(); // prevent browser's default behaviour handling the event(opening the file)
    element.classList.add("drag-over");
};

// function to handle file/image drag leave
window.dragLeave = (element) =>{
    element.classList.remove("drag-over");
};

// function to check if the filetype is an image
const checkImageFile = (fileType) =>{
    const imageExtensions = ["jpg", "jpeg", "png"]; // list of accepted image file types
    let check = false;

    imageExtensions.forEach((extension) => {    // check if the file type contains any of the accepted extensions in the imageExtensions
        if (fileType.includes(extension)){
            check = true;
        }
    });
    return check;
};

// function to remove 'select file' display and send the uploaded image
const removeFileDisplayAndSendImage = (fileAdded) =>{
    addContainer.remove();  // remove the file upload display

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
const sendLoadedImageToServer = (imageFileToSend) => {
    let newXMLRequest = new XMLHttpRequest();
    let newForm = new FormData();

    newForm.append("file", imageFileToSend)     // appending the file uploaded by the user to the form created above

    newXMLRequest.open("POST", "/");
    newXMLRequest.send(newForm);    // send the form data

    newXMLRequest.onload = (e) =>{
        if (newXMLRequest.readyState === 4) {
            if (newXMLRequest.status === 200) { // on successful response
                const response = JSON.parse(newXMLRequest.responseText);    // parsing the response from the server as json instead of string
                detailsContainer.style.display = "block";
                customResultsDiv(response["results"], detailsContainer);    // create results div with the parsed response

                uploadNewBtn.style.display = "block";
                hideLoadingAnimation();

            } else {
              console.error(newXMLRequest.statusText);
            }
        }
    };
};
