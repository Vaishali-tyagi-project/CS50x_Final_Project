

function setDiscount(items)
{
    let item_name = document.getElementById("item");
    let saleType = document.getElementById("sale-type");
    let discount = document.getElementById("discount");
    for (let index = 0; index < items.length; index++) 
    {   
        let item = items[index]
        if (item["itemname"] == item_name.value)
        {
            if (saleType.value == "Retail")
            {
                discount.innerHTML = item["retail_discount"]
            }
            else
            {
                discount.innerHTML = item["wholesale_discount"]
            }
        }    
    }
}