// Run the script when DOM content is loaded
document.addEventListener("DOMContentLoaded", function() {
    // Check response for first question.

    // Change color to green if option is correct.
    let correctOption = document.querySelector(".correct");

    correctOption.addEventListener("click", function() {
        correctOption.style.backgroundColor = "green";
        document.querySelector("#feedback1").innerHTML = "Correct!";
    });

    // Change color to red if option is incorrect.
    let incorrectOption = document.querySelectorAll(".incorrect");

    for (let i = 0; i < incorrectOption.length; i++) {
        incorrectOption[i].addEventListener("click", function() {
            incorrectOption[i].style.backgroundColor = "red";
            document.querySelector("#feedback1").innerHTML = "Incorrect!";
        });
    }

    // Check response for second question.
    document.querySelector("#check").addEventListener("click", function() {

        let input = document.querySelector("input");

        // Change color to green if input is correct.
        if (input.value.toLowerCase() == "denali") {
            input.style.backgroundColor = "green";
            document.querySelector("#feedback2").innerHTML = "Correct!";
        }
        // Change color to red if input is incorrect.
        else {
            input.style.backgroundColor = "red";
            document.querySelector("#feedback2").innerHTML = "Incorrect!";
        }
    });
});
