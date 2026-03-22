from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from trains.models import Train
from .models import Booking
from django.contrib.auth.decorators import login_required

# 🎫 BOOK TICKET (Updated Flow)
@login_required
def book_ticket(request, train_id):
    train = get_object_or_404(Train, id=train_id)

    if request.method == "POST":
        try:
            seats = int(request.POST.get('seats'))
            date = request.POST.get('date')

            if seats <= 0:
                return HttpResponse("❌ Invalid number of seats")

            if seats > train.total_seats:
                return HttpResponse("❌ Not enough seats available")

            # 💾 Save booking with PENDING payment
            booking = Booking.objects.create(
                user=request.user,
                train=train,
                seats_booked=seats,
                journey_date=date,
                payment_status="PENDING"
            )

            # 🔹 Reduce seats immediately (optional, or do after payment)
            train.total_seats -= seats
            train.save()

            # 🔹 Redirect to payment page instead of confirming immediately
            return redirect(f'/payment/{booking.id}/')

        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return render(request, 'book_ticket.html', {'train': train})


# 📄 BOOKING HISTORY
@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking_history.html', {'bookings': bookings})


# ❌ CANCEL BOOKING
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # return seats back
    train = booking.train
    train.total_seats += booking.seats_booked
    train.save()

    booking.delete()

    return redirect('/my-bookings/')


# 💳 Fake Payment Page
@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Redirect if already paid
    if booking.payment_status == "PAID":
        return redirect(f'/payment-success/{booking.id}/')

    if request.method == "POST":
        # Mark as PAID
        booking.payment_status = "PAID"
        booking.save()
        return redirect(f'/payment-success/{booking.id}/')

    return render(request, 'payment.html', {'booking': booking})


# 🎉 Payment Success Page
@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Prevent accessing success page if not paid
    if booking.payment_status != "PAID":
        return redirect(f'/payment/{booking.id}/')

    return render(request, 'payment_success.html', {'booking': booking})