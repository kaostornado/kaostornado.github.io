function saveToFirebase(input) {
    var inputObject = {
        input: input,
    };



    firebase.database().ref('like-counter').push().set(inputObject)
        .then(function (snapshot) {
            sucess();
        }, function (error) {
            console.log('error' + error);
            error();
        })
}

saveToFirebase(input);