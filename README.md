# OutletTVMM
This project will get all the outlet tv from mediamarket oultet website, to check which tv companies in outlet, check loss of profit.
we will be using Python and beautiful soup, then i will try to put in azure data factory from some manipulation then try to use BI Power to make some report out of it.

some important details:

1-TVs in outlet:
https://outlet.mediamarkt.nl/beeld-geluid/televisie-projectie/televisies

2- Get count of tvs from class.level 3 active
and request number on :
<a href="https://outlet.mediamarkt.nl/beeld-geluid/televisie-projectie/televisies" class="list-group-item child_lv3 active">Televisies (229)</a>

3- then Request with the count number:
https://outlet.mediamarkt.nl/beeld-geluid/televisie-projectie/televisies?sort=p.price&order=ASC&limit=NUMBERfromCLASSLVL3

4-getting the data from one product in data , if everything goes well , we will put it in a loop by count of tvs that we took from step 2

class="product-thumb" is the div for product ------------------------------------------------------------------------------------------

*-----price of product (NewPrice,OldPrice)-------*
class price-old : the price in all the spans which you may need to loop.
<div class="price-box has-old-price"> Price div which contains two div class 1. price - old 2. price - new discounted
 <div class="price price-xs price-old length-5" style="visibility: visible;"><span class="p-9">9</span><span class="p-9">9</span><span class="">.</span><span class="p-9 p-ending">9</span><span class="p-9 p-ending">9</span></div>
 <div class="price length-5" style="visibility: visible;"><span class="p-8">8</span><span class="p-4">4</span><span class="">.</span><span class="p-9 p-ending">9</span><span class="p-9 p-ending">9</span></div>
                                                    </div>
*----------------------------*													

*-----discount of product--------*													
div class="discount-percentage text-right center-block"><span>Uw korting</span> 15%</div>
*--------------------------------*

*-----Product Title (Titlename,link) Second Product click get value------*
<a class="product-click" href="https://outlet.mediamarkt.nl/beeld-geluid/televisie-projectie/televisies/samsung-qled-8k-65q800t-2020-ID105103?sort=p.date_added&amp;order=ASC&amp;limit=229" data-product-id="105103" data-product-list="Categorie">SAMSUNG QLED 8K 65Q800T (2020)</a>
*------------------------*

*--------END OF DIV 1--------------------------------------------------------------------------------------


