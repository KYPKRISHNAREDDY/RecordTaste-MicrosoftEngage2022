<h1 align="center">
  <br>
  <img src="https://user-images.githubusercontent.com/65936280/170873022-55e92cd3-1733-4f2e-9e8e-946e572d195e.PNG" alt="RecordTaste" width="120"></a>
  <br>



<br>
 RecordTaste
  <br>
  
</h1>
<h4 align="center">Record Once. Machine Makes Forever . Just Eat And Chill.</h4>
<p align="center">
  <a href="#about">About</a> •
  <a href="#idea">Idea behind Project </a> •
 <a href="#role">Role of the WebApp </a> •
 <a href="#Potential">Features and potential of the WebApp</a> •
  <a href="#ProjectThemeExplaination">Features</a> •
  <a href="#agile">Agile</a>
</p>



<p align="center">
	Developed by : <i> KYP Krishna Reddy</i>
</p>


## About
-Theme of Project

RecordTaste is a web app which  is a full-fledged recommendation E-commerce website containing features like choosing the product, Add to cart, with recommendations based on profile, dish selected, dish ordered, and order history. <br>
This web app has been developed by Krishna Reddy for the Microsoft engage program 2022 (May 4 - May 29)


## Idea
The idea behind the project: As we are in the era of automation, everything is getting automated, from Face recognition to self-driving cars. <br>
Imagine how cool it would be “If cooking also gets automated,” Even though there is no product as such in the current market.
Research is going on in this field, and a high chance of being available shortly.  <br>
Few examples: Molly from Moley robotics, Samsung bot chef  <br>
Let's assume that a machine (which is hypothetical) will have options: fill ingredients, record, cook.  <br> <br>
Fill ingredients: There will be containers for each ingredient required for the dish, which has to be filled manually

Record: 
1.	Press the record option and prepare the dish.
2.	The machine will observe minute details when you are cooking.  <br>
 For example, how many grams of salt is added, the time gap between adding salt and vegetables, the centigrade flame maintained, and many more.  <br>

Cook: </br> 		
		By the inbuilt program of the machine, it starts preparing the dish by taking details from the recording
Next time onwards, there is no need to cook. We just have to load ingredients, provide a recording of the dish, and press the cook option.
It will cook on its own.


## Role Of This WebApp

How amazing it would be "If a person can share their food taste with another person who is in another corner of the world." 
 <br> RecordTaste web app will make this dream come true. <br>
It provides the interface to get programs(recordings) for cooking dishes. Many users/chefs will sell their recordings on our website, and the user will load that code into his machine and it will cook with the same taste as the one in the recorded dish. Meanwhile, we can do other chores and chill.

## Built with
<br><br>
This Web App
<ul>  <b> Bulit with</b>
<ul>
<li>Python</li>
<li>Html</li>
<li> Css</li> 
<li> Javascript</li>
<li> Bootstrap</li>
<li> Django</li>
<li> CSS</li>
<li>Others</li>
</ul>
</ul>
	

 
## Models Used in this Project
![ModelsUsed](https://user-images.githubusercontent.com/65936280/170871182-c15b9451-c629-4254-a5c8-5f477e03be9f.PNG)


## ProjectThemeExplaination 

ProjectThemeExplaination with Pics

![RecordOnce](https://user-images.githubusercontent.com/65936280/170872871-f814c706-6784-4ca1-8369-dbfec56266d7.jpeg)
![Machine Makes Forever](https://user-images.githubusercontent.com/65936280/170872875-a22fd50e-a38d-46b7-9f5b-d179be6c7be2.jpeg)
![Chill and Eat ](https://user-images.githubusercontent.com/65936280/170872881-55699058-3167-4476-b444-f5094533d150.jpeg)



## Features of this WebApp


<ol type="1">
	<li><b>Register: </b></li>
	<ol type="a">
		<li>The user has to register themselves by providing basic details like name, locality, they prefer veg or non-veg etc</li>
	</ol>
  <li> <b>	Login:</b> </li>
	<ol type="a">
		<li>User will login by their credentials </li>
		<li>User can search for an item and see details about it even without logging</li>
		<li>Customized recommendations will be provided only after logging in. </li>
	</ol>
  <li><b> Search:</b> </li>
	<ol type="a">
		<li>User can search food </li>
		<li>Different categories will be provided and user will select Categories on:</li>
		<ol type="i">
			<li>	Time needed for preparation</li>
			<li> Name of Chef </li>
			<li>	Ratings of the chef</li>
			<li>	Veg or non veg</li>
			<li>	 Locality: South Indian, North Indian, Chinese, Italian</li>
			<li>	Price for the recorded video</li>
			<li>	Item type: Breakfast, dinner, refreshment etc</li>
		</ol>
	</ol>
  <li> <b>Add to cart:</b> </li>
	 <ol type="a">
		 <li>Selected food item can be added to cart where details of the order will be visible</li>
	</ol>
  <li><b>Recommendations :</b></li>
	<ol type="a">
		<li>Details during registration is used as primary data to recommend </li>
		<li>Categories used by the user while searching for the food will be used</li>
		<ol type="i">
			<li>	Masala dosa – Details like South Indian food, Breakfast type, approximate time of making, chef details, price range etc will be noted and it will help to customize recommendations</li>
			<li> Chef name and Breakfast type – then the recommendations will have breakfasts prepared by that chef, Breakfasts in general </li>
		</ol>
		<li>The more details user put in while searching the more precise recommendations will be Recommendations will be based on the Item added to the cart </li>
		<li>customized recommendations will be provided only after the user is logged in</li>
	</ol>
</ol>	
	
	
	
	



</br>
</br>

## Features Exploaration in WebApp
	
	
	
	
<ol type="1">
	<li><b>Navigation Bar Updation according to Login Status </b></li>
		<div> <img src="https://user-images.githubusercontent.com/65936280/170947615-96d2ca8b-a623-45d0-9315-aa9204d23c96.jpg" height="420" width="580"></div>
	<br/><br/>
  <li> <b>Register,Login,Profile Filling Option</b> </li>
	<div> <img src="https://user-images.githubusercontent.com/65936280/170948340-16e4e929-b29d-4cd5-a870-96dcdb884cbd.jpg" height="420" width="580"></div>
	<br/><br/>
	
  <li><b> HomePage Recommendations based on Profile Details</b> </li>
	<br/>
	
	
<table>
  <tr>
    <td>Before Login</td>
     <td>After Login</td>
  </tr>
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170947787-dca13934-a3b1-44d9-a27c-b1e552423e0b.jpg"></td>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170948110-373c0213-11bc-4c0b-966b-a341fba42502.jpg"></td>
  </tr>
 </table>
	<br/><br/>
	
  <li> <b>Customised Recommendations based on :</b> </li>
	<br/>
	<ol type="i">
			<li>	Time needed for preparation</li>
			<li> Name of Chef </li>
			<li>	Ratings of the chef</li>
			<li>	Veg or non veg</li>
			<li>	 Locality: South Indian, North Indian, Chinese, Italian</li>
			<li>	Price for the recorded video</li>
			<li>	Item type: Breakfast, dinner, refreshment etc</li>
		</ol>
	<table>
  <tr>
    <td>Before Login</td>
     <td>After Login</td>
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170960351-eb606b8b-1dbb-4951-bb2a-9cd601b5c893.jpg"></td>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170960396-316c1a4c-f56e-4663-ba52-c4b7e98fd02f.jpg"></td>
  </tr>
 </table>
	<br/><br/>
  <li><b>We can Add items To cart by Clicking on AddToCart</b></li>
	<br/>
	<div><img src="https://user-images.githubusercontent.com/65936280/170962233-d6e6992f-edf1-4238-92f1-0505d0ce4aa1.jpg" height="420" width="580" ></div>
	<br/><br/>
	
 <li><b>Clicking Add to Cart </b> </li>
	<br/>

	
<table>
  <tr>
    <td>Without Login<br/></td>
     <td>With Login<br/></td>
  </tr>
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170961402-4a548a85-10a1-40fe-b1fb-4ecd1fb37f8a.jpg"></td>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170961389-c3b29eea-2d31-4f96-888f-b6902d8a1028.jpg"></td>
  </tr>
 </table>
	<br/><br/>
	
  <li> <b>User can Add Multiple Items to the Cart</b> </li>
	<br/>
	<table>
  <tr>
    <td>Before Login</td>
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170970965-3b7134ec-1360-4974-91ab-dbf2930753d4.jpg"></td>
  </tr>
 </table>
	<br/><br/>
	
<table>
  <tr>
    <td><b>8.Webapp Tracks No of items in Cart :<b></td>
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170962382-80b72928-bf9a-47bd-9b15-9d044e8013c8.jpg" height="420" width="580"  ></td>
  </tr>
 </table>
	<br/><br/>
	    
<table>
  <tr>
    <td><b>9. Total_Amount gets Updated on Adding multiple items to the Cart </b></td>
	  <br/>
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170967115-d7c967a0-4809-49bc-900b-5a00edb0443c.jpg" ></td>
  </tr>
 </table>    
	 <br/><br/>
	    
<table>
  <tr>
    <td><b>10.Make Payment Option<b></td>
	    <br/>
	    </tr> 
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170962472-da60e89b-c25e-4d97-9f09-1a37da1377cb.jpg" height="420" width="580" ></td>
   
  </tr>
 </table>
	<br/><br/>
	
<table>
  <tr>
    <td><b>11.After User made Payment,Purchased Items will be added to Orders Page and Cart will get emptied   <b></td>
	    <br/>
	    </tr> 
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170962508-a8ee4c44-0732-4dab-bb5a-21869ce20ea5.jpg" ></td>
   
  </tr>
 </table>
	<br/><br/>
	
	
<table>
  <tr>
    <td><b>12.Dishes Recommendation based on Order History <b></td>
	    <br/>
	    </tr> 
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/65936280/170968001-a7073036-9b14-4c3b-93e2-fbc523d0d2c1.jpg" ></td>
   
  </tr>
 </table>
<br/><br>
	

<br><br>
	
	
<b>Potential of this Webapp if it is developed further :</b>
<ul>
	<li>The web app has the potential to become the best user engaged platform, similar to Youtube, Flipkart, and Amazon.</li>
	<li>Just like Youtube, users can record their cooking and upload it on our website, which will be available to the whole world</li>
	<li>Users who upload Dish Recordings will get money based on how many orders their video gets and the ratings.</li>
	<li>Silver chef, Gold chef etc will be given to uploaders(content creators in our website) to encourage more and more participation</li>
	<li>A feature of customizing food can also be done</li>
	Ex: Only use olive oil 








## Agile

I have adopted the **Scrum** methodology for developing the product. I have divided 25days into four sprints, each consisting of six days. Before every sprint, I used to set a target for the week/sprint and work on it.

**Sprint 1** : The first sprint started on the 4th of May. I dedicated SPRINT 1 entirely to choosing a project out of 3 given by the Microsoft Engage team. Finally, I decided on the 3rd project: The recommendation algorithm web app, after considering multiple factors while selecting a project as a beginner in the tech stack field.
I went through the basics needed to build what I intended to apply to the project. I started planning about how to develop and design my website. I made a basic prototype of the features I was going to include and how. Later I added mandatory features to my website.
After Sprint 1 was over, I took feedback from my friends, Seniors, and family about what they would be looking forward to in a web app. I noted  and worked upon them accordingly.


**Sprint 2 and 3**: Now that I had mandatory features already built and got my mentor assigned, in sprints 2 and 3, I worked on adding additional features to my website. During this phase, I continued taking input from my seniors and friends, then modified my product as per their inputs. I made a manual dataset for my databases, which is a vital factor in this project.


**Sprint 4** : This is the last sprint I had in my development phase. I was close to the delivery date, so I took feedback from friends and others on the UI of my product and then improved it to a great extent. This added beauty to my product and made it delivery ready as well.


## Website demo video
[See demo]([Link Here](https://youtu.be/toMaOVxh1-s) ) - This video has already been submitted with the "Submit your solution form."
<br><br>
## Special Thanks 🙇	
Special thanks to my Microsoft engage mentor for guiding me throughout the program!
To my friends, seniors, and family members for valuable input and Microsoft for this great opportunity





