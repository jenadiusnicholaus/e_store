var updateBtns = document.gelElementsByClassName('update-cart')

//
for(var i - 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.data.product
        var action = this.dataset.action
        console.log('productId', productId,'action:', action)
    })
}