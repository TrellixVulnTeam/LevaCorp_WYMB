import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [

  { path: '', redirectTo: 'elementos-por-habitacion', pathMatch: 'full' },
  { path: 'principal', loadChildren: './pages/principal/principal.module#PrincipalPageModule' },
  { path: 'preferencias', loadChildren: './pages/preferencias/preferencias.module#PreferenciasPageModule' },
  // { path: 'elementos-habitacion', loadChildren: './elementos-habitacion/elementos-habitacion.module#ElementosHabitacionPageModule' },
  { path: 'edificio', loadChildren: './pages/edificio/edificio.module#EdificioPageModule' },
  { path: 'inicio', loadChildren: './pages/inicio/inicio.module#InicioPageModule' },
  { path: 'lectura-qr/:id/:dir', loadChildren: './pages/lectura-qr/lectura-qr.module#LecturaQRPageModule' },
<<<<<<< HEAD
  // tslint:disable-next-line: max-line-length
  { path: 'asociacion-elemento-dispositivo', loadChildren: './pages/asociacion-elemento-dispositivo/asociacion-elemento-dispositivo.module#AsociacionElementoDispositivoPageModule' }
=======
  { path: 'elementos-por-habitacion', loadChildren: './pages/elementos-por-habitacion/elementos-por-habitacion.module#ElementosPorHabitacionPageModule' },
  { path: 'dispositivos-elemento/:id', loadChildren: './pages/dispositivos-elemento/dispositivos-elemento.module#DispositivosElementoPageModule' },
>>>>>>> 0a67cdafce514c5fe4fb130127806fe12a88014d


];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
