function deleteNote(noteId){
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
    window.location.href = "/note";
    })
}

function delete_ip_device(ipId){
    fetch("/delete-ip-device", {
        method: "POST",
        body: JSON.stringify({ ipId: ipId }),
    }).then((_res) => {
    window.location.href = "/ipDevices";
    })
}

function runPythonScript(){
    var pythonScriptPath ="/serverConnection.py";
    subprocess.run(['python', pythonScriptPath]);
}
