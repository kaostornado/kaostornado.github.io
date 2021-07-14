function saveToFirebase(input) {
    var inputObject = {
        input: input,
    };

    firebase.database().ref('like-counter').push().set(inputObject)
        .then(function (snapshot) {
            
        }, function (error) {
            console.log('error' + error);
            error();
        })
}

firebase.firestore().collection('dbskudud')
    .onWrite((change, context) => {

    if (!change.before.exists) {
        // New document Created : add one to count

        db.doc(docRef).update({numberOfDocs: FieldValue.increment(1)});
    
    } else if (change.before.exists && change.after.exists) {
        // Updating existing document : Do nothing

    } else if (!change.after.exists) {
        // Deleting document : subtract one from count

        db.doc(docRef).update({numberOfDocs: FieldValue.increment(-1)});

    }

    return;
});




function addEverythingToDatabase(everything) {
    firebase.firestore().collection("dbskudud").doc("db").get().then((data) => {
        let newData = data.data().word;
        for(let i = 0; i < 100; i++) {
            newData.push({
                score: 0,
                value: everything[i]
            });
        }
        firebase.firestore().collection("dbskudud").doc("db").update({word:newData});
    });
}