document.addEventListener('DOMContentLoaded', function () { // Аналог $(document).ready
        const app = document.getElementById('root');
        const container = document.createElement('div');
        container.setAttribute('id', 'container');
        app.appendChild(container);

        var request = new XMLHttpRequest();
        request.open('GET', '/articles/all/', true);
        request.onload = function () {

            // Begin accessing JSON data here
            var data = JSON.parse(this.response);
            if (request.status >= 200 && request.status < 400) {
                data.forEach(item => {
                    draw_article(data = item, is_full = false);
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

function draw_article(data, is_full) {
    console.log('draw article', data, is_full)

    const article = document.createElement('div');
    article.setAttribute('class', 'article');

    const h1 = document.createElement('h1');
    const open_lnk = document.createElement('a');
    open_lnk.setAttribute('href', '#' + data.id);
    open_lnk.textContent = data.title;

    const p = document.createElement('p');
    var description = data.text || '';
    if (is_full) {
        p.textContent = description
    } else {
        p.textContent = description.substring(0, 300) + ' ...';  // TODO: change to item.description

    }


    const edit_lnk = document.createElement('a');
    edit_lnk.setAttribute('href', '#');
    edit_lnk.textContent = 'edit';

    const rev_lnk = document.createElement('a');
    rev_lnk.setAttribute('href', 'revisions/' + data.id);
    rev_lnk.textContent = 'revisions';

    var container = document.getElementById('container');
    container.appendChild(article);
    article.appendChild(h1);
    h1.appendChild(open_lnk);
    article.appendChild(p);
    article.appendChild(edit_lnk);
    article.appendChild(rev_lnk);

}

$(document).on('click', '.article h1 a', function () {
    // your function here
    var el = $(this)
    console.log('113', el.text());
    var container = $('#container');
    container.empty();

    $.ajax({
        url: 'articles/read/' + el.text() + '/',
        context: document.body
    }).done(function (data) {
        console.log('done', data);
        draw_article(data = data, is_full = true);
    });


});

