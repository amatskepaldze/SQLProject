function like(id){
    $.ajax({
            type: 'POST',
// метод отправки

            url: '/news/' + id + '/like',
// путь к обработчику

            dаta: {},
            dataType: 'text',
            success: function(data){
                $(".answer").html(data);
// при успешном получении ответа от сервера, заносим полученные данные в элемент с классом answer

            },
            error: function(data){
                console.log(data);
// выводим ошибку в консоль

            }
        });
        return false;
    }
