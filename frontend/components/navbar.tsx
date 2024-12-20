import Image from 'next/image';
import Link from 'next/link';
import Logo from '../assets/Logo.svg';
import { Button } from './ui/button';

export default function Navbar() {
    return (
        <header className="sticky top-0 flex h-14 items-left gap-4 border-b bg-foreground px-4 md:px-6">
        <div className="flex w-full justify-between items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
          <div className="flex justify-start">
            <Link href="/"><Image src={Logo} alt="Logo" width={75} height={75} /></Link>
          </div>
          <div className="flex justify-end justify-between">
              <Link href="/auth" className='px-4'><Button>Get Started</Button></Link>
              <Link href="/profile"><Button>Profile</Button></Link>
            </div>
          </div>
          </header>
    )}

