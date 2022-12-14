let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            componentRestrictions: { 'country': ['uk'] },
        })

    // function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}


function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else {
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    // console.log(place)
    var geocoder = new google.maps.Geocoder();
    var address = document.getElementById('id_address').value;

    // console.log(address)
    geocoder.geocode({ 'address': address }, function (results, status) {
        // console.log('results=>', results)
        // console.log('status=>', status)
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            // console.log(latitude);
            // console.log(longitude);
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
            $('#id_address').val(address);
        }
    })
    console.log(place.address_components)

    // loop through the address components and assign other address data
    for (var i = 0; i < place.address_components.length; i++) {
        for (var j = 0; j < place.address_components[i].types.length; j++) {
            // get the country
            if (place.address_components[i].types[j] == 'country') {
                $('#id_country').val(place.address_components[i].long_name);
            }

            // get the state
            if (place.address_components[i].types[j] == 'administrative_area_level_1') {
                $('#id_state').val(place.address_components[i].long_name);
            }

            // get the postcode
            if (place.address_components[i].types[j] == 'postal_code') {
                $('#id_pin_code').val(place.address_components[i].long_name);
            } else {
                $('#id_pin_code').val("");
            }

            // get the city
            if (place.address_components[i].types[j] == 'postal_town') {
                $('#id_city').val(place.address_components[i].long_name);
            }
        }
    }

}


$(document).ready(function () {
    // add to cart
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();

        item_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        // alert(item_id)
        console.log(url)
        data = {
            item_id: item_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    // console.log('raised the error message')
                    swal(response.message, '', 'info').then(function () {
                        window.location = '/login';
                    })
                } else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    // console.log(response.cart_counter['cart_count'])
                    // push response.cart_counter['cart_count'] to the badge above the cart without reload tha page
                    // target the id of the badge above the cart
                    $('#cart_counter').html(response.cart_counter['cart_count'])

                    // push response.cart_counter['cart_count'] to the quanty of the single item  without reload tha page
                    // target the id of the item count above
                    $('#qty-' + item_id).html(response.qty)

                    // subtota, tax and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )

                }


            }


        })
    })

    // place the cart item quantity on load
    $('.item_qty').each(function () {
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        // console.log(qty)
        $('#' + the_id).html(qty)
    })



    // decrease cart
    $('.decrease_cart').on('click', function (e) {
        e.preventDefault();

        item_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');


        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function () {
                        window.location = '/login';
                    })
                } else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-' + item_id).html(response.qty)

                    // subtota, tax and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )

                    // run this only one the user is inside cart page
                    if (window.location.pathname == '/cart/') {
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }

                }

            }
        })
    })



    // DELETE CART ITEM
    $('.delete_cart').on('click', function (e) {
        e.preventDefault();


        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');


        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response)
                if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, "success")

                    // subtota, tax and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )

                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                }
            }
        })
    })



    // delete the cart element if the qty is 0
    function removeCartItem(cartItemQty, cart_id) {
        if (cartItemQty <= 0) {
            // remove the cart item element
            document.getElementById("cart-item-" + cart_id).remove()
        }

    }

    // Check if the cart is empty
    function checkEmptyCart() {
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0) {
            document.getElementById("empty-cart").style.display = "block";
        }
    }


    // apply cart amounts
    function applyCartAmounts(subtotal, tax, grand_total) {
        if (window.location.pathname == '/cart/') {
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)

            // console.log(tax_dict)
            // for(key1 in tax_dict){
            //     console.log(tax_dict[key1])
            //     for(key2 in tax_dict[key1]){
            //         // console.log(tax_dict[key1][key2])
            //         $('#tax-'+key1).html(tax_dict[key1][key2])
            //     }
            // }
        }
    }



})