var e = function(sel){
    return document.querySelector(sel)
}

var log = function(){
    console.log.apply(console, arguments)
}

var ajax = function(method, url, data, responseCallback){
    var r = new XMLHttpRequest()
    r.open(method, url, true)
    r.setRequestHeader('Content-Type', 'application/json')

    r.onreadystatechange = function(){
        if(r.readyState === 4){
            responseCallback(r.response)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}


var apiChangeFollow = function(form, callback){
    var path = '/change_follow'
    ajax('POST', path, form, callback)
}

var bindEventChangeFollow = function(){
    var b = e('#id-btn-follow')
    if (b != undefined){
        var f = e('#id_followed_count')
        b.addEventListener('click', function(){
            d = b.dataset.id
            apiChangeFollow(d, function(r){
                var s = JSON.parse(r)
                if (s.statue == 200){
                    var t = b.text.trim();
                    if(t == '关注'){
                        b.text = '已关注'
                        f.textContent = parseInt(f.textContent) + 1
                    }else if(t == '已关注'){
                        b.text = '关注'
                        f.textContent = parseInt(f.textContent) - 1
                    }
                }
            })
        })
    }

}


var __main = function(){
    bindEventChangeFollow()
}

__main()