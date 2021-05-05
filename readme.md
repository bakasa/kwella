# KWELLA 🚖 - ⚠️ 🚧 👷‍♂️

* ## HOW TO GET THE TESTS RUNNING ON YOUR LOCALHOST?

  * clone the respository.

    ```bash
    git clone https://github.com/yangakandeni/kwella.git
    ```

  * encapsulate the project in an isolated environment

    ```bash
    python3 -m venv venv
    ```

    or

    ```bash
    python -m venv venv
    ```

    on windows.

  * activate your environment
  
    ```bash
    source venv/bin/activate
    ```

    or

    ```bash
    ./venv/Scripts/activate
    ```

    on windows.

  * install project dependencies

    ```bash
    pip install -r requirements.txt
    ```

    and wait until finished.

  * change to the server directory `kwella/server/` with
  
    ```bash
    cd server
    ```

  * run the tests with

    ```bash
    pytest -v
    ```

## What is KWELLA? 🚕 🙋‍♂️ 🙋‍♀️

KWELLA will be an app that connects riders with convenience-taxis in their area. KWELLA's main focus will be providing riders with a platform where they can request **special trips** from convenience-taxi drivers.

### WHAT IS SPECIAL-TRIP?

On a special-trip, the rider will publish details about their _offer_(**how much the rider is willing to pay for the trip**), _location_, _destination_, _departure time_, _type of trip_(**one-way** or **round-trip**)) and the _number of people travelling with_.

This special-trip request will be published to all convenience-taxi drivers on the app and stay "visible" until a driver accepts this request. Once a driver accepts the special-trip (along with its terms), the rider will be able to track the convenience-taxi driver's location _almost_ in real-time. The driver will still be able to accept other special-trips (provided there is consent from the rider).

* #### WHAT IS A ONE-WAY TRIP?

  A one-way trip will be the simplest trip type, where the driver picks up a rider from point A and drops them off at point B.

* #### WHAT IS A ROUND-TRIP (OPTIONAL FEATURE)?

  A round-trip will be a type of trip, where the driver will pick up a rider from point A and drop them off at point B. The driver will either **wait** for the rider to finish his/her/their errands or the driver will **return** at a later time specified by the rider.

### HOW WILL PAYMENT BE HANDLED?

The payment method will be cash only.

### HOW MUCH WILL IT COST?

Riders - KWELLA will be free to download and use for the riders.

Drivers - In order for a convenience-taxi to be active on KWELLA, the **OWNER** of the taxi will have to download and register their taxi(s) on the app. The registration process will requires the taxi's _Taxi Association Number_, _License Plate Number_, _Proof of Residence_, _Bank Statement_, _Pictures of the Taxi (interior & exterior)_, _Picture of License Card_ and _Copy of ID_. The taxi owner would have to agree to a subcription fee of _R100.00_ per month/taxi in order to stay active on the platform.

### HOW WILL A DRIVER GET STARTED?

In order for a driver to get started, he/she/they will be assigned a taxi by a taxi owner. The taxi owner will have to provide the driver's _Name_, _Cellphone Number_ and _Picture of License Card_.

#### HOW WILL A DRIVER GET PAID?

A driver and owner will negotiate the terms of their partnership outside the app. Hence, the app will not concern itself with negotiating rates and resolving disputes.

### WHAT WILL THE ROLE OF TAXI OWNER BE?

The taxi owner will be able to see all the trips (_normal_ and _special_) accepted by the driver throughout the day, with a total estimation of how much the driver should bring by the end of the day. If the taxi owner is not pleased with the driver's performance, the taxi owner will have the option to de-assign the driver from a taxi. Both the driver and the owner will (optionally) rate each other. This rating will be crucial in helping others decide who to partner with (as a driver or owner).

## BOY! THIS SOUNDS AN AWEFUL LOT LIKE UBER AND LYFT! 🙈

Very good observation! It is true that the innovative nature of Uber has made it possible for other similar entities to seek a piece of the pie in this market. However, this project and it's design is no way intended to compete with the giants in the game.

This project (KWELLA) aims to target the local township market in SOUTH AFRICA.

In most (..and by most, I mean all) townships, around SOUTH AFRICA, the taxi industry is...uhm, a very delicate industry. The introduction of giants such as UBER or BOLT were tried and failed, vigorously, due to the fact that these giants, placed themselves as competitors, threatening to annihilate pre-existing taxi infrustructure.

KWELLA's objective, is to enhance the operational nature of these pre-existing taxi infrustructures, by working hand-in-hand with the players in migrating a small (operational) piece into the digital world. KWELLA's end goal is to digitize the entire taxi industry in SOUTH AFRICA.
