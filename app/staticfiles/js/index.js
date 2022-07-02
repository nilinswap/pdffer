console.log("hello world!");


document.addEventListener("DOMContentLoaded", function () { // wait for the dom to load before you start playing with it. 
    main();
});

function main() {
    const input = document.querySelector('input');
    var searchQuery = null;
    input.addEventListener('input', updateValue);
    function updateValue(e) {
      searchQuery = e.target.value;
    }

    const goButton = document.getElementById('search-item-input-submit-button');
    goButton.addEventListener('click', callSearchApi)

    const searchResultUL = document.getElementById('search-item-results');

    function callSearchApi(){
        console.log(searchQuery);
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4){
                var shops = JSON.parse(xhr.responseText);
                console.log('shops', shops)
                liList = []
                if(shops){
                    for (var shop of shops.data) {
                        var liElem = document.createElement("li");
                        liElem.appendChild(document.createTextNode(`name: ${shop.shop_name} address: ${shop.shop_address}`));
                        liList.push(liElem);
                    }
                } else {
                    liList.push(document.createTextNode('No results'));
                }
                console.log('liList', liList)
                for (var ele of liList) {
                    searchResultUL.appendChild(ele);
                }
            }
        };
        xhr.open('GET', '/api/find-shops/?productname=' + searchQuery);
        xhr.send()
    }
}
