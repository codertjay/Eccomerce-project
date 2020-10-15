function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
    const csrftoken =  getToken('csrftoken')


function my_quantity () {
    let post_url = `http://127.0.0.1:8000${url.toLowerCase()}`
    const method = 'POST'
    const formData = new FormData()
    formData.append('slug',product_slug)
    formData.append('action',add)
    $.ajax({
        url:post_url,
        type:method,
        headers : { 'X-CSRFTOKEN':csrftoken},
        data: formData,
            contentType:false,
            cache:false,
            processData: false,
        success: function (response) {
            alert('success',response)
        },
        error: function (response) {
            alert(response.responseText)
            console.log (response)
        }
    }).done(function (response) {
        console.log ('response',response.statusText)
    })



}


function my_event_listener(slug,add,url){
    console.log (slug,add,url)
    let product_slug = slug
    let post_url = `http://127.0.0.1:8000${url.toLowerCase()}`
    const method = 'POST'
    const formData = new FormData()
    formData.append('slug',product_slug)
    formData.append('action',add)
    $.ajax({
        url:post_url,
        type:method,
        headers : { 'X-CSRFTOKEN':csrftoken},
        data: formData,
            contentType:false,
            cache:false,
            processData: false,
        success: function (response) {
            alert('success',response)
        },
        error: function (response) {
            alert(response.responseText)
            console.log (response)
        }
    }).done(function (response) {
        console.log ('response',response.statusText)
    })

}


$(".add-to-cart-form").submit(function (event) {
    event.preventDefault()
    let post_url = $(this).attr("action")
    let request_method = 'Post'
    console.log (post_url)
    console.log (request_method)
    const formData = new FormData()
    const slug = $("#product_slug").val()
    formData.append('slug',slug)
    console.log (formData)
    $.ajax({
        url:post_url,
        type:request_method,
        headers : { 'X-CSRFTOKEN':csrftoken},
        data: formData,
            contentType:false,
            cache:false,
            processData: false,
        success: function (response) {
            alert('success',response)
        },
        error: function (response) {
            alert(response.responseText)
            console.log (response)
        }
    }).done(function (response) {
        console.log ('response',response)
    })
})




$(".item_add_to_cart_form").submit(function (event) {
    event.preventDefault()
    let post_url = $(this).attr("action")
    let request_method = 'Post'
    console.log (post_url)
    console.log (request_method)
    const formData = new FormData()
    const slug = $("#item_add_to_cart_slug").val()
    formData.append('slug',slug)
    console.log (formData)
    $.ajax({
        url:post_url,
        type:request_method,
        headers : { 'X-CSRFTOKEN':csrftoken},
        data: formData,
            contentType:false,
            cache:false,
            processData: false,
        success: function (response) {
            alert(response)
        },
        error: function (response) {
            alert(response.responseText)
            console.log (response)
        }
    }).done(function (response) {
        console.log ('response',response)
    })
})





$(".item_remove_single_from_cart_form").submit(function (event) {
    event.preventDefault()
    console.log ('called ')
    let post_url = $(this).attr("action")
    let request_method = 'Post'
    console.log (post_url)
    console.log (request_method)
    const formData = new FormData()
    const slug = $("#item_add_to_cart_slug").val()
    formData.append('slug',slug)
    console.log (formData)
    $.ajax({
        url:post_url,
        type:request_method,
        headers : { 'X-CSRFTOKEN':csrftoken},
        data: formData,
            contentType:false,
            cache:false,
            processData: false,
        success: function (response) {
            alert(response)
        },
        error: function (response) {
            alert(response.responseText)
            console.log (response)
        }
    }).done(function (response) {
        console.log ('response',response)
    })
})




/*
window.setInterval(function () {
$('#order_item_quantity').ready(function () {
    let get_url = 'http://127.0.0.1:8000/quantity/'
    let request_method = 'Get'
    $.ajax({
        url:get_url,
        type:request_method,
        headers : {
            'content-Type':'application/json',
        },
        success: function (response) {
            alert('response')
            console.log('response',response)
            let quantity = $('#item_quantity')
        },
        error: function (response) {
            // alert('dcnjdvkjndv')
            console.log (response)
        }
    })

})
,10
})
*/








/*

const add_to_cart = document.getElementById('add-to-cart-form')

console.log (getToken('csrftoken'))

function addItemsToCart (event) {
    event.preventDefault()
    console.log ('callled')

    const myForm = event.target
    console.log (myForm)

    const myFormData = new FormData(myForm)
    console.log (myFormData)
    const url = 'http://127.0.0.1:8000/add_to_cart/'
    const xhr = new XMLHttpRequest()
    const csrftoken =  getToken('csrftoken')
    xhr.responseType = 'json'
    xhr.open('POST','http://127.0.0.1:8000/add_to_cart/')
    xhr.setRequestHeader('X-csrf-token',csrftoken)
    xhr.setRequestHeader('HTTP_X_REQUESTED_WITH','XMLHttpRequest')
    xhr.setRequestHeader('X-Requested-with','XMLHttpRequest')
    xhr.onload= function () {
        const my_response = xhr.response
        console.log (my_response)

    }
    xhr.onerror = function () {
        alert('An error occurred pls try again ')
    }
    xhr.send()
}


add_to_cart.addEventListener('submit',addItemsToCart)

*/
