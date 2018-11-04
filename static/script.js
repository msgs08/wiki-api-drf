document.addEventListener('DOMContentLoaded', function () { // Аналог $(document).ready
        const app = document.getElementById('root');
        const container = document.createElement('div');
        container.setAttribute('class', 'container');
        app.appendChild(container);

        var request = new XMLHttpRequest();
        request.open('GET', 'http://127.0.0.1:8000/articles/all/', true);
        request.onload = function () {

            // Begin accessing JSON data here
            var data = JSON.parse(this.response);
            if (request.status >= 200 && request.status < 400) {
                data.forEach(item => {
                    const card = document.createElement('div');
                    card.setAttribute('class', 'card');

                    const h1 = document.createElement('h1');
                    const open_lnk = document.createElement('a');
                    open_lnk.setAttribute('href', 'bbb/' + item.id);
                    open_lnk.textContent = item.title;

                    const p = document.createElement('p');
                    p.textContent = item.title.substring(0, 300) + ' ...';  // TODO: change to item.description


                    const edit_lnk = document.createElement('a');
                    edit_lnk.setAttribute('href', 'aaa/' + item.id);
                    edit_lnk.textContent = 'edit';


                    container.appendChild(card);
                    card.appendChild(h1);
                    h1.appendChild(open_lnk);
                    card.appendChild(p);
                    card.appendChild(edit_lnk);
                });
            }
        };
        request.send();

        const add_el = document.getElementById('add_el');
        add_el.onclick = function () {
            container.textContent = '';
            document.getElementById('uploadForm').style.display = 'block';

        };
    }
);


$(document).on('submit', '#uploadForm', function (e) {
    e.preventDefault();
    $.ajax({
        url: $(this).attr('action'),
        type: 'POST',
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function (data) {
            location.reload();
        },
        error: function (data, textStatus, jqXHR) {
            //process error msg
            console.error(data);
            var errorList = $('ul.errorMessages');
            errorList.empty();

            $("#uploadForm :input").each(function (index, node) {
                var input = $(this);
                if (input.attr('name') in data.responseJSON) {
                    message = data.responseJSON[input.attr('name')];
                    errorList
                        .show()
                        .append('<li><span>' + input.attr('name') + '</span> ' + message + '</li>');
                }
            });
        },
    });
});
