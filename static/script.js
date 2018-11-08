$(function () {
    var ATTR_ID_KEY = 'element-id';
    var HOST = 'http://127.0.0.1:8000/';
    $('.show-form').click(show_form);

    const app = document.getElementById('root');
    const container = document.createElement('div');
    container.setAttribute('id', 'container');
    app.appendChild(container);

    $.ajax({
        url: HOST + 'articles/',
        context: document.body
    }).done(function (data) {
        data.forEach(item => {
            draw_article(data = item, is_full = false);
        });

    });

    function hide_container() {
        var container = $('#container');
        container.empty();
    }

    function show_form() {
        hide_container()
        document.getElementById('uploadForm').style.display = 'block';
    }


    // create new article
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
        open_lnk.setAttribute(ATTR_ID_KEY, data.id);
        open_lnk.textContent = data.title;

        const p = document.createElement('p');
        var description = '';
        if (data.revision.length)
            description = data.revision[0].text
        if (is_full) {
            p.textContent = description
        } else {
            p.textContent = description.substring(0, 300);

        }

        const edit_lnk = document.createElement('a');
        edit_lnk.setAttribute('href', '#');
        edit_lnk.setAttribute('class', 'edit');
        // edit_lnk.setAttribute('class', 'show-form');
        edit_lnk.setAttribute(ATTR_ID_KEY, data.id); // TODO: move element-id up
        edit_lnk.textContent = 'edit';

        const rev_lnk = document.createElement('a');
        rev_lnk.setAttribute('href', '#');
        rev_lnk.setAttribute('class', 'revisions');
        rev_lnk.setAttribute(ATTR_ID_KEY, data.id); // TODO: move element-id up
        rev_lnk.textContent = 'revisions';

        var container = document.getElementById('container');
        container.appendChild(article);
        article.appendChild(h1);
        h1.appendChild(open_lnk);
        article.appendChild(p);
        article.appendChild(edit_lnk);
        article.appendChild(rev_lnk);

    }


    // very terrible function
    function populate_form(form, data) {
        $('[name="title"]', form).val(data.title).attr('readonly', 'readonly');
        $('[name="text"]', form).val(data.revision[0].text);
        $('[type="submit"]', form).val('Update');
        $('#uploadForm').attr('action', '/articles/edit/');
    }

    // read article
    $(document).on('click', '.article h1 a', function () {
        var el = $(this)
        var container = $('#container');
        container.empty();
        $.ajax({
            url: HOST + 'articles/read/' + el.attr(ATTR_ID_KEY) + '/',
            context: document.body
        }).done(function (data) {
            console.log('done', data);
            draw_article(data = data, is_full = true);
        });
    });

    // edit article
    $(document).on('click', '.article a.edit', function () {
        console.log('edit')
        var el = $(this)
        show_form();


        $.ajax({
            url: HOST + 'articles/read/' + el.attr(ATTR_ID_KEY) + '/',
            context: document.body
        }).done(function (data) {
            console.log('done', data);
            form = $('#uploadForm');
            populate_form(form = form, data = data);
        });
    });
    // the article's revisions
    $(document).on('click', '.article a.revisions', function () {
        hide_container();
        var el = $(this);

        $.ajax({
            url: HOST + 'articles/revisions/' + el.attr(ATTR_ID_KEY) + '/',
            context: document.body
        }).done(function (data) {
            const revisions = document.createElement('div');
            const ul = document.createElement('ul');
            const app = document.getElementById('container');

            data.forEach(function (cur_rev) {
                console.log('k,v', cur_rev);
                const li = document.createElement('li');
                var d = new Date(cur_rev.created_at);
                data_text = d.getHours() + ':' + d.getMinutes() + ' ' + d.getDay() + '.' + d.getMonth() + '.' + d.getFullYear();
                li.textContent = '(' + cur_rev.text.substring(0, 30) + '...' + ')' + '  ' + cur_rev.ip_addr + ' ' + data_text;
                ul.appendChild(li);
            });
            app.appendChild(ul);

        });
    });

});
