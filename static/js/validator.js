// function to check if the filetype is an image
const checkImageFile = (fileType) =>{
    const imageExtensions = ["jpg", "jpeg", "png", "webp"]; // list of accepted image file types
    let check = false;

    imageExtensions.forEach((extension) => {    // check if the file type contains any of the accepted extensions in the imageExtensions
        if (fileType.includes(extension)){
            check = true;
        }
    });
    return check;
};

export { checkImageFile };
