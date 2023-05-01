# FBA Order Notifer (WIP)

Paying for software to notify you have new orders can be expensive and bloated with other utility you won't need.

## What is it?

<ul>
  <li> Personal script to notify you when a new order is placed.</li>
  <li> All orders are sent to a discord channel (configurable by the user).</li>
  <li> No longer need to refresh Seller app for new sales.</li>
</ul>

## How does it work?

<ol>
  <li> The script uses the new Amazon SP API to retrieve seller orders.</li>
  <li> New orders are checked at regular intervals.</li>
  <li> If any are detected then they're sent to your specified channel in a neat embed</li>
  <li> Order details include Order no., ASIN, order total etc.</li>
 </ol>
  
 ## Getting Started
 
 To get started with the script you will need the following:
 <ul>
  <li> A seller account with a LWA refresh token to login to your account.</li>
  <li> A discord account with a server and channel (with a webhook URL) to send your notifications to.</li>
  <li> Python 3.X installed on your system.</li>
 </ul>
 
 Steps:
 <ol>
  <li> You will need to first create a Selling Partner Developer account to get your Refresh token alongside your client ID and secret key</li>
  <li> Add the refresh token to the "config.json" and the ID + secret keys to the config_loader.py</li>
  <li> Save the files and execute the file by either clicking on it or with the command <code>python3 main.py</code> while in the directory.
  <li> Now let the script do its thing in the background while the orders come in!</li>
 </ol>
 
 [Guide will be updated as project develops]
 
 ![Image of a test webhook sent](https://cdn.discordapp.com/attachments/659152859480195073/1102710499403104347/image.png)
