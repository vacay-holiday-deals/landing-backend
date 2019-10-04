# class that contains different type of messages
class Data():
    def body(data):
        body = """
            <body>
            <div class="container" style="width: 100%; margin: 1rem 0; border: 0.5px solid #eee; border-radius: 5px;">
            <div class="header" style="height: 15vh;width: 100%;background: #eee;position: relative;">
                <div class="logo" style="height: 10vh; width: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px;">
                <img
                    src="https://res.cloudinary.com/lostvane/image/upload/v1570009762/image002.png"
                    alt="logo"
                    style="height: 100%;object-fit: contain;"
                />
                </div>
            </div>

            <div class="body" style="padding: 10px; width: 80%; margin: 1rem 10%;">
                <ul class="list-group"  style="padding: 10px; list-style: none;">
                <li class="list-item" style="padding: 5px 10px; border-left: 2px solid yellow; margin: 1rem 0;">
                    Name <br />
                    <span>{name}</span>
                </li>
                <li class="list-item" style="padding: 5px 10px; border-left: 2px solid yellow; margin: 1rem 0;">
                    Email <br />
                    <span>{email}</span>
                </li>
                <li class="list-item" style="padding: 5px 10px; border-left: 2px solid yellow; margin: 1rem 0;">
                    Nationality <br />
                    <span>{nationality}</span>
                </li>
                <li class="list-item" style="padding: 5px 10px; border-left: 2px solid yellow; margin: 1rem 0;">
                    Number <br />
                    <span>{number}</span>
                </li>
                <li class="list-item" style="padding: 5px 10px; border-left: 2px solid yellow; margin: 1rem 0;">
                    Departure <br />
                    <span>{departure}</span>
                </li>
                <li class="list-item" style="padding: 5px 10px; border-left: 2px solid yellow; margin: 1rem 0;">
                    Destination <br />
                    <span>{destination}</span>
                </li>
                <li class="list-item" style="padding: 5px 10px; border-left: 2px solid yellow; margin: 1rem 0;">
                    Adults <br />
                    <span>{adults}</span>
                </li>
                <li class="list-item" style="padding: 5px 10px; border-left: 2px solid yellow; margin: 1rem 0;">
                    Children <br />
                    <span>{children}</span>
                </li>
                <li class="list-item" style="padding: 5px 10px; border-left: 2px solid yellow; margin: 1rem 0;">
                    budget <br />
                    <span>{budget}</span>
                </li>
                <li class="list-item" style="padding: 5px 10px; border-left: 2px solid yellow; margin: 1rem 0;">
                    Additional Information <br />
                    <span>{info}</span>
                </li>
                </ul>
            </div>
            <div class="footer" style="background:#000411; height: 15vh; padding: 10px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; color: #999; font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; font-size: 14px;">
                <p>
                For more information, contact us as info@vacay.co.ke or
                booking@info.co.ke
                </p>
                <hr style="width: 40%; border: 0.5px solid #999; margin: 0 30%;" />
                <p>&copy; offers.vacay.co.ke 2019 All Rights Reserved</p>
            </div>
            </div>
        </body>
        """
        my_email_body = body.format(name=data['Name'], email=data['Email'], nationality=data['Nationality'], number=data['Number'], departure=data['Departure'],
                                    destination=data['Destination'], adults=data['Adult'], children=data['Children'], budget=data['Budget'], info=data['Addinfo'])
        return my_email_body
