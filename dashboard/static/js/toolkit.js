



function save_and_download_content_as_file(text, file_name) {

    var blob = new Blob([text], {type: 'text/csv'});

    save_to_file(blob, file_name);

}

function save_to_file(input_blob, input_filename) {
    if (window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveOrOpenBlob(input_blob, input_filename);
    } else {
        const a = document.createElement('a');
        document.body.appendChild(a);
        const url_ = window.URL.createObjectURL(input_blob);
        a.href = url_;
        a.download = input_filename;
        a.click();
        setTimeout(() => {
            window.URL.revokeObjectURL(url_);
            document.body.removeChild(a);
        }, 0)
    }
}



function js_full_copy(input_object){
    return JSON.parse(JSON.stringify(input_object));
}


function make_titled(input_string) {
    const string_p = input_string.replaceAll("_", ' ');
    return string_p.toLowerCase().split(' ').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ');
}


function get_string_of_datetime(){
    return new Date().toLocaleString()
}


// function new_uuid() {
//     return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
//         var tmp = Math.random() * 16 | 0, value = c == 'x' ? tmp : (tmp & 0x3 | 0x8);
//         return value.toString(16);
//     });
// }
//
//
// function belongs_to(element, my_arr) {
//     return (my_arr.indexOf(element) > -1);
// }

