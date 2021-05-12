from nmigen import *
from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock

class Stream(Record):
    def __init__(self, width, **kwargs):
        Record.__init__(
            self, [('data', width), ('valid', 1), ('ready', 1)], **kwargs)

    def accepted(self):
        return self.valid & self.ready
    
    class Driver:
        def __init__(self, clk, dut, prefix):
            self.clk = clk
            self.data = getattr(dut, prefix + 'data')
            self.valid = getattr(dut, prefix + 'valid')
            self.ready = getattr(dut, prefix + 'ready')

        # To the adder
        async def send(self, data):
            self.valid <= 1
            for d in data:
                self.data <= d
                await RisingEdge(self.clk)
                while self.ready.value == 0:
                    await RisingEdge(self.clk)
            self.valid <= 0

        # From the adder
        async def recv(self, count):
            self.ready <= 1
            data = []
            for _ in range(count):
                await RisingEdge(self.clk)
                while self.valid.value == 0:
                    await RisingEdge(self.clk)
                data.append(self.data.value.integer)
            self.ready <= 0
            return data


class Adder(Elaboratable):
    def __init__(self, width):
        self.a = Stream(width, name='a')
        self.b = Stream(width, name='b')
        self.r = Stream(width, name='r')
        self.aux = Signal(1)

    def elaborate(self, platform):
        m = Module()
        sync = m.d.sync
        comb = m.d.comb

        with m.If(self.r.accepted()):
            sync += self.r.valid.eq(0)
            comb += self.aux.eq(0)

        with m.If(self.a.valid & self.b.valid & self.r.ready):
            sync += self.r.data.eq(self.a.data + self.b.data)
            comb += self.aux.eq(1)
        

        with m.If(self.aux & self.a.accepted() & self.b.accepted()):
            sync += self.r.valid.eq(1)

        comb += self.a.ready.eq(self.a.valid & self.b.valid & self.aux)
        comb += self.b.ready.eq(self.a.valid & self.b.valid & self.aux)       
        return m

# Simulation block
async def init_test(dut):
    cocotb.fork(Clock(dut.clk, 10, 'ns').start())
    dut.rst <= 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst <= 0

@cocotb.test()
async def burst(dut):
    await init_test(dut)

    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')
    
    width = len(dut.a__data)
    N = (2 ** width-1)  
    mask = int('1' * width, 2)
    sign_a = [1+j for j in range(N)]
    sign_b = [2 for _ in range(N)]
    expected_1 = []
    
    # The first sign i expect
    for i in range(0, N):
        expected_1 = expected_1 + [(sign_a[i]+sign_b[i]) & mask]
    # I must do the truncation (& mask) by the size of the variables

    # For the validation test, I want to prove that if any of 
    # the ports is not valid, the data is not lost. For that use the line
    # "await RisingEdge(dut.clk)" delaying the sending of signals

    # Send the sign_a to the port a
    cocotb.fork(stream_input_a.send(sign_a))

    # wait a period
    await RisingEdge(dut.clk)

    # Send the sign_b to the port b
    cocotb.fork(stream_input_b.send(sign_b))

    # wait for the first output sign
    recved_1 = await stream_output.recv(N)

    # wait two periods
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    # Swap the signals for test
    # Send the sign_b to the port a
    cocotb.fork(stream_input_b.send(sign_a))

    # wait a period
    await RisingEdge(dut.clk)
    # Send the sign_b to the port a
    cocotb.fork(stream_input_a.send(sign_b))

    # wait for the second output sign
    recved_2 = await stream_output.recv(N)

    # Test codition formal verification
    assert recved_1 + recved_2 == expected_1 + expected_1


if __name__ == '__main__':
    core = Adder(5)
    run(
        core, 'adder',
        ports=[
            *list(core.a.fields.values()),
            *list(core.b.fields.values()),
            *list(core.r.fields.values())
        ],
        vcd_file='./VCD/adder.vcd'
    )
