# KWELLA - The convenience-taxi hailing app

## What is KWELLA?

KWELLA is an app that connects commuters with convenience-taxis in their area. The app has two ride options, a **normal-trip** or a **special-trip**.

### WHAT IS A NORMAL-TRIP?

On a normal-trip, a commuter publishes their _current location_, _departure time_, _ride status_ (**whether or not they've accepted a ride**) and _destination_. All convenience-taxis, within a certain radius, will be able to see the commuter's location, status and destination, ontop of that, each convenience-taxi will be able to see other taxis within the same radius.

A a willing taxi driver will send a "ride with me" request to the commuter. This request will publish details, such as number plate, taxi association number (if available) and ratings to the commuter. The commuter will choose to accept or reject the request made by the convenience-taxi. If a commuter does not respond (within 3s) to a "ride with me" request from a taxi, the request will automatically be rejected and the commuter will be invisible to the taxi, from which the request was sent. Other convenience-taxis will still be able to see the commuter.

Once a commuter accepts or cancels a ride, the commuter will be "invisible" from the app. At the end of the journey, the commuter will be able to rate the experience on the convenience-taxi.

### WHAT IS SPECIAL-TRIP?

On a special-trip, the commuter will publish details about their _offer_(**how much the commuter is willing to pay for the trip**), _location_, _destination_, _departure time_, _type of trip_(**one-way** or **round-trip**)) and the _number of people travelling with_.
This special-trip request will be published to all convenience-taxi drivers on the app and stay "visible" until a driver accepts this request. Once a driver accepts the special-trip (along with its terms), the commuter will be able to track the convenience-taxi driver's location _almost_ in real-time. Even though the commuter will be "invisible" from the app, this particular driver will still be "visible" and able to accept other trips.

* #### WHAT IS A ONE-WAY TRIP?

  A one-way trip is a type of trip, where the driver picks up a commuter from a pick up location and drops them off at their desired destination. The terms of the one-way trip will be determined by the trip category (_i.e._ **_normal-trip_** or **_special-trip_**).

* #### WHAT IS A ROUND-TRIP (OPTIONAL FEATURE)?

  A round-trip is a type of special-trip, where the convenience-taxi driver will pick up a commuter from their location and drop them off at their desired destination. The driver will either **wait** for the commuter to finish his/her/their errands or the driver will **return** at a later time specified by the commuter.

### HOW IS PAYMENT HANDLED?

The current payment method is cash only. Once KWELLA gains popularity and users (both riders and drivers) request an in-app payment feauture, it will be implemented.

### HOW MUCH DOES IT COST?

Commuters - KWELLA is free to download and use for the commuters.

Convenince-Taxi - In order for a convenience-taxi to be active on KWELLA, the **OWNER** of the taxi must download and register their taxi(s) on the app. The registration process requires the taxi's _Taxi Association Number_, _License Plate Number_, _Proof of Residence_, _Bank Statement_, _Pictures of the Taxi (interior & exterior)_, _Picture of License Card_ and _Copy of ID_. The taxi owner must agree to a subcription fee of _R200.00_ per month/taxi in order to stay active on the platform.

### HOW DOES A DRIVER GET STARTED?

In order for a driver to get started, he/she/they must be assigned a taxi by a taxi owner. The taxi owner must provide the driver's _Name_, _Cellphone Number_ and _Picture of License Card_. To login and start accepting trips, the driver needs to provide the _Taxi Association Number_ (of their assigned taxi) and their phone number (used when assigning them to said taxi).

#### HOW DOES A DRIVER GET PAID?

A driver and owner will negotiate the terms of their partnership outside the app. Hence, the app will not concern itself with negotiating rates and resolving disputes.

### WHAT CAN THE TAXI OWNER DO?

The taxi owner can see all the trips (_normal_ and _special_) accepted by the driver throughout the day, with a total estimation of how much the driver should bring by the end of the day. If the taxi owner is not pleased with the driver's performance, the taxi owner can de-assign the driver from a taxi. Both the driver and the owner can (optionally) rate each other on a monthly basis or at the end of their partnership. This rating is crucial in helping others descide who to partner with (as a driver or owner).