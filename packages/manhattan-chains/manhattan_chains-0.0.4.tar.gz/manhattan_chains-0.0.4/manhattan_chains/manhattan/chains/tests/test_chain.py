from manhattan.chains import Chain


def test_init():
    """Initialize a chain"""
    chain = Chain(['foo', 'bar'])
    assert chain.links == ['foo', 'bar']

def test_call():
    """Call the chain executing the linked functions"""
    chain = Chain([
        'foo',
        'bar',
        [
            ['zee'],
            ['omm']
        ]
    ])

    @chain.link
    def foo(state):
        pass

    @chain.link
    def bar(state):
        if state.bar:
            return 'bar'
        return state.zee

    @chain.link
    def zee(state):
        return 'zee'

    @chain.link
    def omm(state):
        return 'omm'

    # Check the chain exectution works as expected
    assert chain(bar=False, zee=False) == 'omm'
    assert chain(bar=False, zee=True) == 'zee'
    assert chain(bar=True, zee=True) == 'bar'

def test_links():
    """Get a copy of the links in the chain"""
    links = [
        'foo',
        'bar',
        [
            ['zee'],
            ['omm']
        ]
    ]
    chain = Chain(links)

    # Check the links are the same
    assert chain.links == links

    # Check the links are a copy (deepcopy)
    assert chain.links is not links
    assert chain.links[2] is not links[2]
    assert chain.links[2][0] is not links[2][0]
    assert chain.links[2][1] is not links[2][1]

def test_copy():
    """Copy the chain"""
    chain = Chain(['foo', 'bar'])

    @chain.link
    def foo(state):
        pass

    @chain.link
    def bar(state):
        pass

    chain_copy = chain.copy()

    # Check the chain is the same
    assert chain_copy.links == chain.links
    assert chain_copy._funcs == chain._funcs

    # Check the chain is a copy
    assert chain_copy is not chain
    assert chain_copy._links is not chain._links
    assert chain_copy._funcs is not chain._funcs

def test_get_link():
    """Get the function mapped to the named link(s) in the chain"""
    chain = Chain(['foo', 'bar'])

    @chain.link
    def foo(state):
        pass

    assert chain.get_link('foo') == foo

def test_set_links():
    """Map a function to the named link(s) in the chain"""
    chain = Chain(['foo', 'bar'])

    # Set the link using the functions name
    def foo(state):
        pass

    chain.set_link(foo)
    assert chain.get_link('foo') == foo

    # Set the link using a specified name
    def zee(state):
        pass

    chain.set_link(zee, name='bar')
    assert chain.get_link('bar') == zee

def test_link():
    """Map a function to the named link(s) in the chain"""
    chain = Chain(['foo', 'bar'])

    # Set the link using the functions name
    @chain.link
    def foo(state):
        pass

    assert chain.get_link('foo') == foo

    # Set the link using a specified name
    @chain.link(name='bar')
    def zee(state):
        pass

    assert chain.get_link('bar') == zee

def test_update():
    """Update the links for the chain"""
    chain = Chain(['foo', 'bar'])

    @chain.link
    def foo(state):
        pass

    @chain.link
    def bar(state):
        pass

    chain.update(['foo', 'zee'])

    # Check the link structure has been updated
    assert chain.links == ['foo', 'zee']