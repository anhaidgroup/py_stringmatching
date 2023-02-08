# Simplified knockoff of nose.tools.raises
def raises(exc_type):
    def deco(f):
        def raises_wrapper(self):
            with self.assertRaises(exc_type):
                return f(self)
        return raises_wrapper
    return deco
