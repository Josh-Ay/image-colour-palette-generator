const container = document.querySelector(".container-fluid");

const customErrorDiv = (message, containerElement) =>{
    // create a new div and add a class to style it
    const errorDiv = document.createElement("div");
    errorDiv.className = "error-div";

    // create a paragraph element and add a class to style it
    const errorParagraph = document.createElement("p");
    errorParagraph.className = "error-message";

    // creates a text with the 'message' passed into the function
    const errorMsg = document.createTextNode(message);

    //  append the text to the paragraph element(created above)
    errorParagraph.appendChild(errorMsg);

    // create a button element and add a class to style it
    const okBtn = document.createElement("button");
    okBtn.classList.add("btn", "error-message-btn");

    // create button text and append it to the button
    const okBtnContent = document.createTextNode("OK");
    okBtn.appendChild(okBtnContent);

    // append the paragraph and button to the div created
    errorDiv.appendChild(errorParagraph);
    errorDiv.appendChild(okBtn);

    // insert the div into the document
    document.body.insertBefore(errorDiv, containerElement);

    // remove the div created from the document on click outside of the div
    window.addEventListener("click", function(e){
        if (!errorDiv.contains(e.target)){
            errorDiv.remove();
        }
    });

    // remove the div created from the document on click of the button
    okBtn.addEventListener("click", function(){errorDiv.remove()})
};

const customDiv = (message, backgroundColor, containerElement, textColor) =>{
    // create a new div and add a class and the 'color passed' parameter to style it
    const customDiv = document.createElement("div");
    customDiv.className = "color-copied-div";
    customDiv.style.background = backgroundColor;

    // create a h1 element and add a class to style it
    const copyMessage = document.createElement("h1");
    copyMessage.className = "copy-message";

    // creates a text with the 'message' passed into the function
    const copyMessageTxt = document.createTextNode(message);

    //  append the text to the h1 element(created above)
    copyMessage.appendChild(copyMessageTxt);

    // append the h1 to the div created
    customDiv.appendChild(copyMessage);

    if (typeof(textColor) !== "undefined"){
        customDiv.style.color = textColor;
    };


    // insert the div into the document
    document.body.insertBefore(customDiv, containerElement);

    // remove the div created from the document after 1s
    setTimeout(() => {
        customDiv.remove();
    }, 1000);
};


const customResultsDiv = (resultList, containerElement) =>{
    let newFragment = document.createDocumentFragment();    // creating a document fragment
    for(let i=0 ; i < resultList.length; i++ ){
        // creating the required elements
        let resultBox = document.createElement("div");
        let colorDiv = document.createElement("div");
        let color = document.createElement("div");
        let colorCodeDiv = document.createElement("div");
        let colorCodeParagraph = document.createElement("p");
        let colorCodeHoverParagraph = document.createElement("p");
        let colorCodeCopyParagraph = document.createElement("p");
        let colorPercentDiv = document.createElement("div");
        let colorPercentParagraph = document.createElement("p");

        // styling the created elements by adding classes
        resultBox.classList.add("result-box", "result");
        colorDiv.className = "color";
        color.className = "color-display";
        colorCodeDiv.className = "color-code";
        colorPercentDiv.className = "color-percentage";
        colorCodeCopyParagraph.className = "color-code-text";

        // creating text nodes to hold the 'color_code' value in the list passed
        let codeText = document.createTextNode(resultList[i]["color_code"]);
        let codeTextHover = document.createTextNode("Copy");
        let codeTextCopy = document.createTextNode(resultList[i]["color_code"]);
        let codeTextStr = resultList[i]["color_code"];

        // appending a div with the background of the color code and the color text to the 'colorDiv' (container)
        color.style.background = resultList[i]["color_code"];
        colorCodeHoverParagraph.appendChild(codeTextHover);

        // check if the color has more than 2f's in its hex code i.e a very light color
        if (((codeTextStr.match(/f/g) || []).length) > 2){
            colorCodeHoverParagraph.style.color = "#000";   // black color
        };

        colorCodeCopyParagraph.appendChild(codeTextCopy);
        color.appendChild(colorCodeHoverParagraph);
        color.appendChild(colorCodeCopyParagraph);
        colorDiv.appendChild(color);

        // attaching the color code text to the 'colorCodeParagraph' paragraph element and appending the paragraph to the div
        colorCodeParagraph.appendChild(codeText);
        colorCodeDiv.appendChild(colorCodeParagraph);

        // creating a text node to hold the 'percent_count' value in the list passed and attaching it to the 'colorPercentParagraph' paragraph
        let percentText = document.createTextNode(resultList[i]["percent_count"]);
        colorPercentParagraph.appendChild(percentText);
        colorPercentDiv.appendChild(colorPercentParagraph);

        // appending the individual divs to the parent div which is 'resultBox' div
        resultBox.appendChild(colorDiv);
        resultBox.appendChild(colorCodeDiv);
        resultBox.appendChild(colorPercentDiv);

        newFragment.appendChild(resultBox);     // appending the 'resultBox' div to the document fragment

        color.addEventListener("mouseover", (e) => { // to show the hex text on mouse hover
            e.target.style.boxShadow = "10px 0 80px rgba(0, 0, 0, .5)";
            colorCodeHoverParagraph.style.display = "block";
        });

        color.addEventListener("mouseleave", (e) => {    // to hide the hex text on mouse leave
            e.target.style.boxShadow = "none";
            colorCodeHoverParagraph.style.display = "none";
        });

        color.addEventListener("click", (e) => { // to copy the hex text on click
            const colorToCopy = e.target.parentElement.children[1].innerText;

            navigator.clipboard.writeText(colorToCopy);

            // check if the 'colorToCopy' has more than 2f's in its hex code(i.e a very light color) and if so set the color of text within to "black"
            if (((colorToCopy.match(/f/g) || []).length) > 2){
                customDiv(`Copied ${colorToCopy}`, colorToCopy, container, "#000");
            }else{
                customDiv(`Copied ${colorToCopy}`, colorToCopy, container);
            }
        });
    }

    containerElement.appendChild(newFragment);  // appending the document fragment to the 'containerElement' passed
};

export {customErrorDiv, customResultsDiv};
