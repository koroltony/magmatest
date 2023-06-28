import magma as m
import mantle

class ShiftRegister(m.Circuit):
    io = m.IO(
        input=m.In(m.Bit),
        clk=m.In(m.Clock),
        reset=m.In(m.AsyncReset),
        enable=m.In(m.Enable),
        dir=m.In(m.Bit),
        output=m.Out(m.Bits[8])
    )

    reg = m.Register(m.Bits[8], init=0, has_enable=True, reset_type=m.AsyncReset)()

    # Shift register logic with enable using mantle.mux
    shifted_data = mantle.mux(
        [m.concat(io.input, reg.O[:-1]), m.concat(reg.O[1:], io.input)],
        io.dir
    )
    enable_cond = m.bit(io.enable) & m.bit(io.clk)  # Enable condition using bitwise AND
    reg.I @= mantle.mux([reg.O, shifted_data], enable_cond)

    # Output logic
    io.output @= reg.O

    # Reset logic
    reg.RESET @= io.reset