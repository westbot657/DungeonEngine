# pylint: disable=W,R,C
class UIElement:
    def _event(self, editor, X, Y):
        raise NotImplementedError(f"Please implement '_event' for {self}")
    def _update(self, editor, X, Y):
        raise NotImplementedError(f"Please implement '_update' for {self}")
    def get_collider(self):
        raise NotImplementedError(f"Please implement 'get_collider' for {self}")
