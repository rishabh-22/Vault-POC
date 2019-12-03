var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
// variables to check if form inputs are valid and if a request is being processed for registration
var form_is_good_to_post = true
var server_is_processing = false

// Regex patterns used for input validations
var regx_patts = {
    first_name: [/^[A-Za-z]+$/, '*Only alphabetical characters allowed'],
    last_name: [/^[A-Za-z]+$/, '*Only alphabetical characters allowed'],
    username: [/^(\D)+(\w)*((\.(\w)+)?)+@(\D)+(\w)*((\.(\D)+(\w)*)+)?(\.)[a-z]{2,}$/, '*Only valid emails allowed'],
    password: [/^(?=(.*[a-zA-Z].*){2,})(?=.*\d.*)(?=.*\W.*)[a-zA-Z0-9\S]{8,15}$/, '*Must be 8-15 characters with at least one uppercase letter, lower case letter, digit, and special character'],
    phone: [/^\d{10}$/, '*Must be a 10 digit phone number']
}

// Check if both password fields have same inputs
function ConfirmPassword() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("secondpassword").value;
    if (password === confirmPassword) {
        return true
    }
    $('#error-confirmpassword').html('*Passwords must match')
    $('#secondpassword').css('border', '1px solid red')
    return false
}

// Validates field value after onclick event of submit button
function ValidateField(name, val) {
    if (!regx_patts[name][0].test(val)) {
        form_is_good_to_post = false
        if (name==='first_name') {
            $('#'+name).css('margin-bottom', '0px')
        }
        $('#'+name).css('border', '1px solid red')
        $('#error-'+name).html(regx_patts[name][1])
    }
}

// Initiate validation process after onclick of signup button
$('#signup-button').click(function() {
    form_is_good_to_post = true
    inputs = $('.signup').children('.post')
    // Dynamically add required property to HTML field elements in case user has manually overwritten
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].required = true
    }
})


// Upon valid form submission check executes ajax request with form data
var form = document.querySelector('.signup').onsubmit = function (evt) {
    evt.preventDefault()
    // Empty error message if shown before due to invalid inputs
    $('#response-error').html('')
    // Run second round of form validation using regex
    for (let i = 0; i < inputs.length; i++) {
        if (regx_patts.hasOwnProperty(inputs[i].name)) {
            ValidateField(inputs[i].name, inputs[i].value)
        }
    }
    // Send request if passwords match, if form inputs regex validated, and request is not already processing
    if (ConfirmPassword() && form_is_good_to_post && !server_is_processing) {
        // Show loader above submit button to let user know their request has been sent
        $('.loader').css('display', 'block')
        // Set variable to indicate a request is processing so that user can't send another until processing complete
        server_is_processing = true
        // Grab all the form data to send in post request
        form_data = $('.signup').children('.post')
        // new HttpRequest instance
        var xmlhttp = new XMLHttpRequest();
        // declare asynchronous function to be called after a response has been recieved
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                // once response is received we can set variable to let future requests be sent
                server_is_processing = false
                // remove loader as request is no longer being processed
                $('.loader').css('display', 'none')
                // parse json response object into a js accessible object
                res = JSON.parse(this.responseText)
                // to execute if user is successfully registered
                if (res['success']) {
                    // remove error messages from form validation if any previously present
                    $('#response-error').css('display', 'none')
                    $('#register-form-container').css('display', 'none')
                    // Give success message on DOM
                    $('#confirmation-message').css('display', 'block')
                    $('#confirmation-title').html('Success')
                    // Scroll to top so user can see their success
                    document.body.scrollTop = document.documentElement.scrollTop = 0;
                }
                // two errors could possibly come: 1) Username is already taken 2) Email failed to send
                else {
                    $('#response-error').html('An account with this email already exists!')
                }
            }
        };
        // parse form data into an object which is JSON compatible
        obj_to_post = new Object()
        for (let i = 0; i < form_data.length; i++) {
            obj_to_post[form_data[i].name] = form_data[i].value
        }
        // attach register api url to request object
        xmlhttp.open("POST", "/api/user/register/");
        // indicate that json object is being sent in request body via the request header
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        // set csrf token in header so django server accepts the request
        xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
        // send request with form data in request body
        xmlhttp.send(JSON.stringify(obj_to_post));

    }
    // if user has some invalid regex validations in their form found then display an error message, assuming
    // a request is not already processing
    else if (!server_is_processing) {
        $('#response-error').html("1 or more fields contain invalid inputs...")
    }
};
