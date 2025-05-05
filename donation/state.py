# Context class
class DonationContext:
    def __init__(self, donation):
        self.donation = donation
        self.state = self._get_state_instance()

    def _get_state_instance(self):
        state_map = {
            'available': AvailableState,
            'reserved': ReservedState,
            'collected': CollectedState,
            'delivered': DeliveredState,
        }
        state_class = state_map.get(self.donation.status)
        if state_class:
            return state_class(self)
        else:
            raise ValueError(f"Invalid donation status: {self.donation.status}")

    def change_state(self, new_status):
        self.donation.status = new_status
        self.donation.save()
        self.state = self._get_state_instance()

    def reserve(self):
        return self.state.reserve()

    def collect(self):
        return self.state.collect()

    def deliver(self):
        return self.state.deliver()

# Base State class
class DonationState:
    def __init__(self, context):
        self.context = context
        self.donation = context.donation

    def reserve(self):
        raise ValueError("Cannot be reserved in current state.")

    def collect(self):
        raise ValueError("Cannot be collected in current state.")

    def deliver(self):
        raise ValueError("Cannot be delivered in current state.")

# Concrete State classes
class AvailableState(DonationState):
    def reserve(self):
        self.context.change_state('reserved')
        return True

class ReservedState(DonationState):
    def collect(self):
        self.context.change_state('collected')
        return True

    def deliver(self):
        self.context.change_state('delivered')
        return True

class CollectedState(DonationState):
    pass  # Final state after collection; no further actions

class DeliveredState(DonationState):
    pass  # No operations allowed after delivery

