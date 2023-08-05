if VERSION >= v"0.4-"
  __precompile__()
end

module GR

using Compat

if VERSION > v"0.5-"
  if Sys.KERNEL == :NT
    const os = :Windows
  else
    const os = Sys.KERNEL
  end
else
  const os = OS_NAME
end

if VERSION < v"0.4-"
  typealias AbstractString String
  typealias UInt8 Uint8
  typealias UInt32 Uint32
else
  const None = Union{}
end

export
  opengks,
  closegks,
  inqdspsize,
  openws,
  closews,
  activatews,
  deactivatews,
  clearws,
  updatews,
  polyline,
  polymarker,
  text,
  inqtext,
  fillarea,
  cellarray,
  spline,
  gridit,
  setlinetype,
  setlinewidth,
  setlinecolorind,
  setmarkertype,
  setmarkersize,
  setmarkercolorind,
  settextfontprec,
  setcharexpan,
  setcharspace,
  settextcolorind,
  setcharheight,
  setcharup,
  settextpath,
  settextalign,
  setfillintstyle,
  setfillstyle,
  setfillcolorind,
  setcolorrep,
  setscale,
  setwindow,
  setviewport,
  selntran,
  setclip,
  setwswindow,
  setwsviewport,
  createseg,
  copyseg,
  redrawsegws,
  setsegtran,
  closeseg,
  emergencyclosegks,
  updategks,
  setspace,
  textext,
  inqtextext,
  axes,
  grid,
  grid3d,
  verrorbars,
  herrorbars,
  polyline3d,
  polymarker3d,
  axes3d,
  titles3d,
  surface,
  contour,
  setcolormap,
  colormap,
  inqcolor,
  inqcolorfromrgb,
  hsvtorgb,
  tick,
  validaterange,
  adjustlimits,
  adjustrange,
  beginprint,
  beginprintext,
  endprint,
  ndctowc,
  wctondc,
  wc3towc,
  drawrect,
  fillrect,
  drawarc,
  fillarc,
  drawpath,
  setarrowstyle,
  setarrowsize,
  drawarrow,
  readimage,
  drawimage,
  importgraphics,
  setshadow,
  settransparency,
  setcoordxform,
  begingraphics,
  endgraphics,
  getgraphics,
  drawgraphics,
  mathtex,
  selectcontext,
  trisurface,
  gradient,
  quiver,
  # Convenience functions
  jlgr,
  figure,
  hold,
  subplot,
  plot,
  oplot,
  semilogx,
  semilogy,
  loglog,
  scatter,
  stem,
  histogram,
  contourf,
  wireframe,
  plot3,
  scatter3,
  title,
  xlabel,
  ylabel,
  legend,
  xlim,
  ylim,
  savefig,
  meshgrid,
  peaks,
  imshow,
  isosurface,
  cart2sph,
  sph2cart,
  polar,
  trisurf,
  libGR3,
  gr3,
  isinline,
  inline,
  show


mime_type = None
figure_count = None
msgs = None
have_clear_output = isinteractive() && isdefined(Main, :IJulia) &&
                    isdefined(Main.IJulia, :clear_output)

function __init__()
    global libGR, libGR3
    if "GRDIR" in keys(ENV)
        grdir = ENV["GRDIR"]
    elseif isdir(joinpath(homedir(), "gr"), "fonts")
        grdir = joinpath(homedir(), "gr")
    else
        grdir = None
        for d in ("/opt", "/usr/local", "/usr")
            if isdir(joinpath(d, "gr", "fonts"))
                grdir = joinpath(d, "gr")
                break
            end
        end
    end
    if grdir == None
        grdir = joinpath(Pkg.dir(), "GR", "deps", "gr")
    end
    ENV["GRDIR"] = grdir
    ENV["GKS_FONTPATH"] = grdir
    if contains(grdir, "site-packages")
        const libGR = joinpath(grdir, "libGR.so")
        ENV["GKS_FONTPATH"] = grdir
    elseif os != :Windows
        const libGR = joinpath(grdir, "lib", "libGR.so")
    else
        const libGR = joinpath(grdir, "libGR.dll")
    end
    if !isfile(libGR)
        println("Unable to load GR framework runtime environment")
        exit(-1)
    end
    const libGR3 = replace(libGR, "libGR", "libGR3")
end

function opengks()
  ccall( (:gr_opengks, libGR),
        Void,
        ()
        )
end

function closegks()
  ccall( (:gr_closegks, libGR),
        Void,
        ()
        )
end

function inqdspsize()
  mwidth = Cdouble[0]
  mheight = Cdouble[0]
  width = Cint[0]
  height = Cint[0]
  ccall( (:gr_inqdspsize, libGR),
        Void,
        (Ptr{Cdouble}, Ptr{Cdouble}, Ptr{Cint}, Ptr{Cint}),
        mwidth, mheight, width, height)
  return mwidth[1], mheight[1], width[1], height[1]
end

function openws(workstation_id::Int, connection, workstation_type::Int)
  ccall( (:gr_openws, libGR),
        Void,
        (Int32, Ptr{Cchar}, Int32),
        workstation_id, connection, workstation_type)
end

function closews(workstation_id::Int)
  ccall( (:gr_closews, libGR),
        Void,
        (Int32, ),
        workstation_id)
end

function activatews(workstation_id::Int)
  ccall( (:gr_activatews, libGR),
        Void,
        (Int32, ),
        workstation_id)
end

function deactivatews(workstation_id::Int)
  ccall( (:gr_deactivatews, libGR),
        Void,
        (Int32, ),
        workstation_id)
end

function clearws()
  global msgs
  try
    if isinline() && have_clear_output
      IJulia.clear_output(true)
    end
  catch
    have_clear_output = false
  end
  if msgs != None
    begingraphics("")
  end
  ccall( (:gr_clearws, libGR),
        Void,
        ()
        )
end

function updatews()
  global msgs
  if msgs != None
    endgraphics()
  end
  ccall( (:gr_updatews, libGR),
        Void,
        ()
        )
end

function polyline(x, y)
  assert(length(x) == length(y))
  n = length(x)
  ccall( (:gr_polyline, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{Float64}),
        n, convert(Vector{Float64}, x), convert(Vector{Float64}, y))
end

function polymarker(x, y)
  assert(length(x) == length(y))
  n = length(x)
  ccall( (:gr_polymarker, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{Float64}),
        n, convert(Vector{Float64}, x), convert(Vector{Float64}, y))
end

function latin1(string)
  b = convert(Array{UInt8}, string)
  s = zeros(UInt8, length(string))
  len = 0
  mask = 0
  for c in b
    if c != 0xc2 && c != 0xc3
      len += 1
      s[len] = c | mask
    end
    if c == 0xc3
      mask = 0x40
    else
      mask = 0
    end
  end
  return s
end

function text(x::Real, y::Real, string)
  ccall( (:gr_text, libGR),
        Void,
        (Float64, Float64, Ptr{UInt8}),
        x, y, latin1(string))
end

function inqtext(x, y, string)
  tbx = Cdouble[0, 0, 0, 0]
  tby = Cdouble[0, 0, 0, 0]
  ccall( (:gr_inqtext, libGR),
        Void,
        (Float64, Float64, Ptr{UInt8}, Ptr{Cdouble}, Ptr{Cdouble}),
        x, y, latin1(string), tbx, tby)
  return tbx, tby
end

function fillarea(x, y)
  assert(length(x) == length(y))
  n = length(x)
  ccall( (:gr_fillarea, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{Float64}),
        n, convert(Vector{Float64}, x), convert(Vector{Float64}, y))
end

function cellarray(xmin::Real, xmax::Real, ymin::Real, ymax::Real, dimx::Int, dimy::Int, color)
  if ndims(color) == 2
    color = reshape(color, dimx * dimy)
  end
  ccall( (:gr_cellarray, libGR),
        Void,
        (Float64, Float64, Float64, Float64, Int32, Int32, Int32, Int32, Int32, Int32, Ptr{Int32}),
        xmin, xmax, ymin, ymax, dimx, dimy, 1, 1, dimx, dimy, convert(Vector{Int32}, color))
end

function spline(x, y, m, method)
  assert(length(x) == length(y))
  n = length(x)
  ccall( (:gr_spline, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{Float64}, Int32, Int32),
        n, convert(Vector{Float64}, x), convert(Vector{Float64}, y), m, method)
end

function gridit(xd, yd, zd, nx, ny)
  assert(length(xd) == length(yd) == length(zd))
  nd = length(xd)
  x = Cdouble[1 : nx ;]
  y = Cdouble[1 : ny ;]
  z = Cdouble[1 : nx*ny ;]
  ccall( (:gr_gridit, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}, Int32, Int32, Ptr{Cdouble}, Ptr{Cdouble}, Ptr{Cdouble}),
        nd, convert(Vector{Float64}, xd), convert(Vector{Float64}, yd), convert(Vector{Float64}, zd), nx, ny, x, y, z)
  return x, y, z
end

function setlinetype(style::Int)
  ccall( (:gr_setlinetype, libGR),
        Void,
        (Int32, ),
        style)
end

function setlinewidth(width::Real)
  ccall( (:gr_setlinewidth, libGR),
        Void,
        (Float64, ),
        width)
end

function setlinecolorind(color::Int)
  ccall( (:gr_setlinecolorind, libGR),
        Void,
        (Int32, ),
        color)
end

function setmarkertype(mtype::Int)
  ccall( (:gr_setmarkertype, libGR),
        Void,
        (Int32, ),
        mtype)
end

function setmarkersize(mtype::Real)
  ccall( (:gr_setmarkersize, libGR),
        Void,
        (Float64, ),
        mtype)
end

function setmarkercolorind(color::Int)
  ccall( (:gr_setmarkercolorind, libGR),
        Void,
        (Int32, ),
        color)
end

function settextfontprec(font::Int, precision::Int)
  ccall( (:gr_settextfontprec, libGR),
        Void,
        (Int32, Int32),
        font, precision)
end

function setcharexpan(factor::Real)
  ccall( (:gr_setcharexpan, libGR),
        Void,
        (Float64, ),
        factor)
end

function setcharspace(spacing::Real)
  ccall( (:gr_setcharspace, libGR),
        Void,
        (Float64, ),
        spacing)
end

function settextcolorind(color::Int)
  ccall( (:gr_settextcolorind, libGR),
        Void,
        (Int32, ),
        color)
end

function setcharheight(height::Real)
  ccall( (:gr_setcharheight, libGR),
        Void,
        (Float64, ),
        height)
end

function setcharup(ux::Real, uy::Real)
  ccall( (:gr_setcharup, libGR),
        Void,
        (Float64, Float64),
        ux, uy)
end

function settextpath(path::Int)
  ccall( (:gr_settextpath, libGR),
        Void,
        (Int32, ),
        path)
end

function settextalign(horizontal::Int, vertical::Int)
  ccall( (:gr_settextalign, libGR),
        Void,
        (Int32, Int32),
        horizontal, vertical)
end

function setfillintstyle(style::Int)
  ccall( (:gr_setfillintstyle, libGR),
        Void,
        (Int32, ),
        style)
end

function setfillstyle(index::Int)
  ccall( (:gr_setfillstyle, libGR),
        Void,
        (Int32, ),
        index)
end

function setfillcolorind(color::Int)
  ccall( (:gr_setfillcolorind, libGR),
        Void,
        (Int32, ),
        color)
end

function setcolorrep(index::Int, red::Real, green::Real, blue::Real)
  ccall( (:gr_setcolorrep, libGR),
        Void,
        (Int32, Float64, Float64, Float64),
        index, red, green, blue)
end

function setscale(options::Int)
  ccall( (:gr_setscale, libGR),
        Void,
        (Int32, ),
        options)
end

function setwindow(xmin::Real, xmax::Real, ymin::Real, ymax::Real)
  ccall( (:gr_setwindow, libGR),
        Void,
        (Float64, Float64, Float64, Float64),
        xmin, xmax, ymin, ymax)
end

function setviewport(xmin::Real, xmax::Real, ymin::Real, ymax::Real)
  ccall( (:gr_setviewport, libGR),
        Void,
        (Float64, Float64, Float64, Float64),
        xmin, xmax, ymin, ymax)
end

function selntran(transform::Int)
  ccall( (:gr_selntran, libGR),
        Void,
        (Int32, ),
        transform)
end

function setclip(indicator::Int)
  ccall( (:gr_setclip, libGR),
        Void,
        (Int32, ),
        indicator)
end

function setwswindow(xmin::Real, xmax::Real, ymin::Real, ymax::Real)
  ccall( (:gr_setwswindow, libGR),
        Void,
        (Float64, Float64, Float64, Float64),
        xmin, xmax, ymin, ymax)
end

function setwsviewport(xmin::Real, xmax::Real, ymin::Real, ymax::Real)
  ccall( (:gr_setwsviewport, libGR),
        Void,
        (Float64, Float64, Float64, Float64),
        xmin, xmax, ymin, ymax)
end

function createseg(segment::Int)
  ccall( (:gr_createseg, libGR),
        Void,
        (Int32, ),
        segment)
end

function copyseg(segment::Int)
  ccall( (:gr_copyseg, libGR),
        Void,
        (Int32, ),
        segment)
end

function redrawsegws()
  ccall( (:gr_redrawsegws, libGR),
        Void,
        ()
        )
end

function setsegtran(segment::Int, fx::Real, fy::Real, transx::Real, transy::Real, phi::Real, scalex::Real, scaley::Real)
  ccall( (:gr_setsegtran, libGR),
        Void,
        (Int32, Float64, Float64, Float64, Float64, Float64, Float64, Float64),
        segment, fx, fy, transx, transy, phi, scalex, scaley)
end

function closeseg()
  ccall( (:gr_closeseg, libGR),
        Void,
        ()
        )
end

function emergencyclosegks()
  ccall( (:gr_emergencyclosegks, libGR),
        Void,
        ()
        )
end

function updategks()
  ccall( (:gr_updategks, libGR),
        Void,
        ()
        )
end

function setspace(zmin::Real, zmax::Real, rotation::Int, tilt::Int)
  ccall( (:gr_setspace, libGR),
        Void,
        (Float64, Float64, Int32, Int32),
        zmin, zmax, rotation, tilt)
end

function textext(x::Real, y::Real, string)
  ccall( (:gr_textext, libGR),
        Void,
        (Float64, Float64, Ptr{UInt8}),
        x, y, latin1(string))
end

function inqtextext(x::Real, y::Real, string)
  tbx = Cdouble[0, 0, 0, 0]
  tby = Cdouble[0, 0, 0, 0]
  ccall( (:gr_inqtextext, libGR),
        Void,
        (Float64, Float64, Ptr{UInt8}, Ptr{Cdouble}, Ptr{Cdouble}),
        x, y, latin1(string), tbx, tby)
  return tbx, tby
end

function axes(x_tick::Real, y_tick::Real, x_org::Real, y_org::Real, major_x::Int, major_y::Int, tick_size::Real)
  ccall( (:gr_axes, libGR),
        Void,
        (Float64, Float64, Float64, Float64, Int32, Int32, Float64),
        x_tick, y_tick, x_org, y_org, major_x, major_y, tick_size)
end

function grid(x_tick::Real, y_tick::Real, x_org::Real, y_org::Real, major_x::Int, major_y::Int)
  ccall( (:gr_grid, libGR),
        Void,
        (Float64, Float64, Float64, Float64, Int32, Int32),
        x_tick, y_tick, x_org, y_org, major_x, major_y)
end

function grid3d(x_tick::Real, y_tick::Real, z_tick::Real, x_org::Real, y_org::Real, z_org::Real, major_x::Int, major_y::Int, major_z::Int)
  ccall( (:gr_grid3d, libGR),
        Void,
        (Float64, Float64, Float64, Float64, Float64, Float64, Int32, Int32, Int32),
        x_tick, y_tick, z_tick, x_org, y_org, z_org, major_x, major_y, major_z)
end

function verrorbars(px, py, e1, e2)
  assert(length(px) == length(py) == length(e1) == length(e2))
  n = length(px)
  ccall( (:gr_verrorbars, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}),
        n, convert(Vector{Float64}, px), convert(Vector{Float64}, py), convert(Vector{Float64}, e1), convert(Vector{Float64}, e2))
end

function herrorbars(px, py, e1, e2)
  assert(length(px) == length(py) == length(e1) == length(e2))
  n = length(px)
  ccall( (:gr_herrorbars, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}),
        n, convert(Vector{Float64}, px), convert(Vector{Float64}, py), convert(Vector{Float64}, e1), convert(Vector{Float64}, e2))
end

function polyline3d(px, py, pz)
  assert(length(px) == length(py) == length(pz))
  n = length(px)
  ccall( (:gr_polyline3d, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}),
        n, convert(Vector{Float64}, px), convert(Vector{Float64}, py), convert(Vector{Float64}, pz))
end

function polymarker3d(px, py, pz)
  assert(length(px) == length(py) == length(pz))
  n = length(px)
  ccall( (:gr_polymarker3d, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}),
        n, convert(Vector{Float64}, px), convert(Vector{Float64}, py), convert(Vector{Float64}, pz))
end

function axes3d(x_tick::Real, y_tick::Real, z_tick::Real, x_org::Real, y_org::Real, z_org::Real, major_x::Int, major_y::Int, major_z::Int, tick_size::Real)
  ccall( (:gr_axes3d, libGR),
        Void,
        (Float64, Float64, Float64, Float64, Float64, Float64, Int32, Int32, Int32, Float64),
        x_tick, y_tick, z_tick, x_org, y_org, z_org, major_x, major_y, major_z, tick_size)
end

function titles3d(x_title, y_title, z_title)
  ccall( (:gr_titles3d, libGR),
        Void,
        (Ptr{UInt8}, Ptr{UInt8}, Ptr{UInt8}),
        latin1(x_title), latin1(y_title), latin1(z_title))
end

function surface(px, py, pz, option::Int)
  nx = length(px)
  ny = length(py)
  if typeof(pz) == Function
    f = pz
    pz = Float64[f(x,y) for y in py, x in px]
  end
  nz = length(pz)
  if ndims(pz) == 1
    out_of_bounds = nz != nx * ny
  elseif ndims(pz) == 2
    out_of_bounds = size(pz)[1] != nx || size(pz)[2] != ny
  else
    out_of_bounds = true
  end
  if !out_of_bounds
    if ndims(pz) == 2
      pz = reshape(pz, nx * ny)
    end
    ccall( (:gr_surface, libGR),
          Void,
          (Int32, Int32, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}, Int32),
          nx, ny, convert(Vector{Float64}, px), convert(Vector{Float64}, py), convert(Vector{Float64}, pz), option)
  else
    println("Arrays have incorrect length or dimension.")
  end
end

function contour(px, py, h, pz, major_h::Int)
  nx = length(px)
  ny = length(py)
  nh = length(h)
  if typeof(pz) == Function
    f = pz
    pz = Float64[f(x,y) for y in py, x in px]
  end
  nz = length(pz)
  if ndims(pz) == 1
    out_of_bounds = nz != nx * ny
  elseif ndims(pz) == 2
    out_of_bounds = size(pz)[1] != nx || size(pz)[2] != ny
  else
    out_of_bounds = true
  end
  if !out_of_bounds
    if ndims(pz) == 2
      pz = reshape(pz, nx * ny)
    end
    ccall( (:gr_contour, libGR),
          Void,
          (Int32, Int32, Int32, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}, Int32),
          nx, ny, nh, convert(Vector{Float64}, px), convert(Vector{Float64}, py), convert(Vector{Float64}, h), convert(Vector{Float64}, pz), major_h)
  else
    println("Arrays have incorrect length or dimension.")
  end
end

function setcolormap(index::Int)
  ccall( (:gr_setcolormap, libGR),
        Void,
        (Int32, ),
        index)
end

function colormap()
  ccall( (:gr_colormap, libGR),
        Void,
        ()
        )
end

function inqcolor(color::Int)
  rgb = Cint[0]
  ccall( (:gr_inqcolor, libGR),
        Void,
        (Int32, Ptr{Int32}),
        color, rgb)
  return rgb
end

function inqcolorfromrgb(red::Real, green::Real, blue::Real)
  color = ccall( (:gr_inqcolorfromrgb, libGR),
                Int32,
                (Float64, Float64, Float64),
                red, green, blue)
  return color
end

function hsvtorgb(h::Real, s::Real, v::Real)
  r = Cdouble[0]
  g = Cdouble[0]
  b = Cdouble[0]
  ccall( (:gr_hsvtorgb, libGR),
        Void,
        (Float64, Float64, Float64, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}),
        h, s, v, r, g, b)
  return r[1], g[1], b[1]
end

function tick(amin::Real, amax::Real)
  return ccall( (:gr_tick, libGR),
               Float64,
               (Float64, Float64),
               amin, amax)
end

function validaterange(amin::Real, amax::Real)
  return ccall( (:gr_validaterange, libGR),
               Int32,
               (Float64, Float64),
               amin, amax)
end

function adjustlimits(amin::Real, amax::Real)
  _amin = Cdouble[amin]
  _amax = Cdouble[amax]
  ccall( (:gr_adjustlimits, libGR),
        Void,
        (Ptr{Float64}, Ptr{Float64}),
        _amin, _amax)
  return _amin[1], _amax[1]
end

function adjustrange(amin::Real, amax::Real)
  _amin = Cdouble[amin]
  _amax = Cdouble[amax]
  ccall( (:gr_adjustrange, libGR),
        Void,
        (Ptr{Float64}, Ptr{Float64}),
        _amin, _amax)
  return _amin[1], _amax[1]
end

function beginprint(pathname)
  ccall( (:gr_beginprint, libGR),
        Void,
        (Ptr{Cchar}, ),
        pathname)
end

function beginprintext(pathname, mode, fmt, orientation)
  ccall( (:gr_beginprintext, libGR),
        Void,
        (Ptr{Cchar}, Ptr{Cchar}, Ptr{Cchar}, Ptr{Cchar}),
        pathname, mode, fmt, orientation)
end

function endprint()
  ccall( (:gr_endprint, libGR),
        Void,
        ()
        )
end

function ndctowc(x::Real, y::Real)
  _x = Cdouble[x]
  _y = Cdouble[y]
  ccall( (:gr_ndctowc, libGR),
        Void,
        (Ptr{Float64}, Ptr{Float64}),
        _x, _y)
  return _x[1], _y[1]
end

function wctondc(x::Real, y::Real)
  _x = Cdouble[x]
  _y = Cdouble[y]
  ccall( (:gr_wctondc, libGR),
        Void,
        (Ptr{Float64}, Ptr{Float64}),
        _x, _y)
  return _x[1], _y[1]
end

function wc3towc(x::Real, y::Real, z::Real)
  _x = Cdouble[x]
  _y = Cdouble[y]
  _z = Cdouble[z]
  ccall( (:gr_wc3towc, libGR),
        Void,
        (Ptr{Float64}, Ptr{Float64}, Ptr{Float64}),
        _x, _y, _z)
  return _x[1], _y[1], _z[1]
end

function drawrect(xmin::Real, xmax::Real, ymin::Real, ymax::Real)
  ccall( (:gr_drawrect, libGR),
        Void,
        (Float64, Float64, Float64, Float64),
        xmin, xmax, ymin, ymax)
end

function fillrect(xmin::Real, xmax::Real, ymin::Real, ymax::Real)
  ccall( (:gr_fillrect, libGR),
        Void,
        (Float64, Float64, Float64, Float64),
        xmin, xmax, ymin, ymax)
end

function drawarc(xmin::Real, xmax::Real, ymin::Real, ymax::Real, a1::Int, a2::Int)
  ccall( (:gr_drawarc, libGR),
        Void,
        (Float64, Float64, Float64, Float64, Int32, Int32),
        xmin, xmax, ymin, ymax, a1, a2)
end

function fillarc(xmin::Real, xmax::Real, ymin::Real, ymax::Real, a1::Int, a2::Int)
  ccall( (:gr_fillarc, libGR),
        Void,
        (Float64, Float64, Float64, Float64, Int32, Int32),
        xmin, xmax, ymin, ymax, a1, a2)
end

function drawpath(points, codes, fill::Int)
  len = length(points)
  ccall( (:gr_drawpath, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{UInt8}, Int32),
        len, convert(Vector{Float64}, points), convert(Vector{UInt8}, codes), fill)
end

function setarrowstyle(style::Int)
  ccall( (:gr_setarrowstyle, libGR),
        Void,
        (Int32, ),
        style)
end

function setarrowsize(size::Real)
  ccall( (:gr_setarrowsize, libGR),
        Void,
        (Float64, ),
        size)
end

function drawarrow(x1::Real, y1::Real, x2::Real, y2::Real)
  ccall( (:gr_drawarrow, libGR),
        Void,
        (Float64, Float64, Float64, Float64),
        x1, y1, x2, y2)
end

function readimage(path)
  width = Cint[0]
  height = Cint[0]
  data = Array(Ptr{UInt32}, 1)
  ccall( (:gr_readimage, libGR),
        Void,
        (Ptr{Cchar}, Ptr{Int32}, Ptr{Int32}, Ptr{Ptr{UInt32}}),
        path, width, height, data)
  if width[1] > 0 && height[1] > 0
    img = pointer_to_array(data[1], (width[1], height[1]))
    return Int(width[1]), Int(height[1]), img
  else
    return 0, 0, zeros(UInt32, 0)
  end
end

function drawimage(xmin::Real, xmax::Real, ymin::Real, ymax::Real, width::Int, height::Int, data, model::Int = 0)
  if ndims(data) == 2
    data = reshape(data, width * height)
  end
  ccall( (:gr_drawimage, libGR),
        Void,
        (Float64, Float64, Float64, Float64, Int32, Int32, Ptr{UInt32}, Int32),
        xmin, xmax, ymin, ymax, width, height, convert(Vector{UInt32}, data), model)
end

function importgraphics(path)
  ccall( (:gr_importgraphics, libGR),
        Void,
        (Ptr{Cchar}, ),
        path)
end

function setshadow(offsetx::Real, offsety::Real, blur::Real)
  ccall( (:gr_setshadow, libGR),
        Void,
        (Float64, Float64, Float64),
        offsetx, offsety, blur)
end

function settransparency(alpha::Real)
  ccall( (:gr_settransparency, libGR),
        Void,
        (Float64, ),
        alpha)
end

function setcoordxform(mat)
  assert(length(mat) == 6)
  ccall( (:gr_setcoordxform, libGR),
        Void,
        (Ptr{Float64}, ),
        convert(Vector{Float64}, mat))
end

function begingraphics(path)
  ccall( (:gr_begingraphics, libGR),
        Void,
        (Ptr{Cchar}, ),
        path)
end

function endgraphics()
  ccall( (:gr_endgraphics, libGR),
        Void,
        ()
        )
end

function getgraphics()
  string = ccall( (:gr_getgraphics, libGR),
                 Ptr{Cchar},
                 (),
                 )
  return bytestring(string)
end

function drawgraphics(string)
  ret = ccall( (:gr_drawgraphics, libGR),
              Int32,
              (Ptr{Cchar}, ),
              string)
  return int(ret)
end

function mathtex(x::Real, y::Real, string)
  ccall( (:gr_mathtex, libGR),
        Void,
        (Float64, Float64, Ptr{Cchar}),
        x, y, string)
end

ASF_BUNDLED = 0
ASF_INDIVIDUAL = 1

NOCLIP = 0
CLIP = 1

COORDINATES_WC = 0
COORDINATES_NDC = 1

INTSTYLE_HOLLOW = 0
INTSTYLE_SOLID = 1
INTSTYLE_PATTERN = 2
INTSTYLE_HATCH = 3

TEXT_HALIGN_NORMAL = 0
TEXT_HALIGN_LEFT = 1
TEXT_HALIGN_CENTER = 2
TEXT_HALIGN_RIGHT = 3
TEXT_VALIGN_NORMAL = 0
TEXT_VALIGN_TOP = 1
TEXT_VALIGN_CAP = 2
TEXT_VALIGN_HALF = 3
TEXT_VALIGN_BASE = 4
TEXT_VALIGN_BOTTOM = 5

TEXT_PATH_RIGHT = 0
TEXT_PATH_LEFT = 1
TEXT_PATH_UP = 2
TEXT_PATH_DOWN = 3

TEXT_PRECISION_STRING = 0
TEXT_PRECISION_CHAR = 1
TEXT_PRECISION_STROKE = 2

LINETYPE_SOLID = 1
LINETYPE_DASHED = 2
LINETYPE_DOTTED = 3
LINETYPE_DASHED_DOTTED = 4
LINETYPE_DASH_2_DOT = -1
LINETYPE_DASH_3_DOT = -2
LINETYPE_LONG_DASH = -3
LINETYPE_LONG_SHORT_DASH = -4
LINETYPE_SPACED_DASH = -5
LINETYPE_SPACED_DOT = -6
LINETYPE_DOUBLE_DOT = -7
LINETYPE_TRIPLE_DOT = -8

MARKERTYPE_DOT = 1
MARKERTYPE_PLUS = 2
MARKERTYPE_ASTERISK = 3
MARKERTYPE_CIRCLE = 4
MARKERTYPE_DIAGONAL_CROSS = 5
MARKERTYPE_SOLID_CIRCLE = -1
MARKERTYPE_TRIANGLE_UP = -2
MARKERTYPE_SOLID_TRI_UP = -3
MARKERTYPE_TRIANGLE_DOWN = -4
MARKERTYPE_SOLID_TRI_DOWN = -5
MARKERTYPE_SQUARE = -6
MARKERTYPE_SOLID_SQUARE = -7
MARKERTYPE_BOWTIE = -8
MARKERTYPE_SOLID_BOWTIE = -9
MARKERTYPE_HOURGLASS = -10
MARKERTYPE_SOLID_HGLASS = -11
MARKERTYPE_DIAMOND = -12
MARKERTYPE_SOLID_DIAMOND = -13
MARKERTYPE_STAR = -14
MARKERTYPE_SOLID_STAR = -15
MARKERTYPE_TRI_UP_DOWN = -16
MARKERTYPE_SOLID_TRI_RIGHT = -17
MARKERTYPE_SOLID_TRI_LEFT = -18
MARKERTYPE_HOLLOW_PLUS = -19
MARKERTYPE_OMARK = -20
MARKERTYPE_PENTAGON = -21
MARKERTYPE_HEXAGON = -22
MARKERTYPE_HEPTAGON = -23
MARKERTYPE_OCTAGON = -24
MARKERTYPE_STAR_4 = -25
MARKERTYPE_STAR_5 = -26
MARKERTYPE_STAR_6 = -27
MARKERTYPE_STAR_7 = -28
MARKERTYPE_STAR_8 = -29
MARKERTYPE_VLINE = -30
MARKERTYPE_HLINE = -31

OPTION_X_LOG = 1
OPTION_Y_LOG = 2
OPTION_Z_LOG = 4
OPTION_FLIP_X = 8
OPTION_FLIP_Y = 16
OPTION_FLIP_Z = 32

OPTION_LINES = 0
OPTION_MESH = 1
OPTION_FILLED_MESH = 2
OPTION_Z_SHADED_MESH = 3
OPTION_COLORED_MESH = 4
OPTION_CELL_ARRAY = 5
OPTION_SHADED_MESH = 6
OPTION_HEATMAP = 7

MODEL_RGB = 0
MODEL_HSV = 1

COLORMAP_UNIFORM = 0
COLORMAP_TEMPERATURE = 1
COLORMAP_GRAYSCALE = 2
COLORMAP_GLOWING = 3
COLORMAP_RAINBOWLIKE = 4
COLORMAP_GEOLOGIC = 5
COLORMAP_GREENSCALE = 6
COLORMAP_CYANSCALE = 7
COLORMAP_BLUESCALE = 8
COLORMAP_MAGENTASCALE = 9
COLORMAP_REDSCALE = 10
COLORMAP_FLAME = 11
COLORMAP_BROWNSCALE = 12
COLORMAP_PILATUS = 13
COLORMAP_AUTUMN = 14
COLORMAP_BONE = 15
COLORMAP_COOL = 16
COLORMAP_COPPER = 17
COLORMAP_GRAY = 18
COLORMAP_HOT = 19
COLORMAP_HSV = 20
COLORMAP_JET = 21
COLORMAP_PINK = 22
COLORMAP_SPECTRAL = 23
COLORMAP_SPRING = 24
COLORMAP_SUMMER = 25
COLORMAP_WINTER = 26
COLORMAP_GIST_EARTH = 27
COLORMAP_GIST_HEAT = 28
COLORMAP_GIST_NCAR = 29
COLORMAP_GIST_RAINBOW = 30
COLORMAP_GIST_STERN = 31
COLORMAP_AFMHOT = 32
COLORMAP_BRG = 33
COLORMAP_BWR = 34
COLORMAP_COOLWARM = 35
COLORMAP_CMRMAP = 36
COLORMAP_CUBEHELIX = 37
COLORMAP_GNUPLOT = 38
COLORMAP_GNUPLOT2 = 39
COLORMAP_OCEAN = 40
COLORMAP_RAINBOW = 41
COLORMAP_SEISMIC = 42
COLORMAP_TERRAIN = 43
COLORMAP_VIRIDIS = 44
COLORMAP_INFERNO = 45
COLORMAP_PLASMA = 46
COLORMAP_MAGMA = 47

FONT_TIMES_ROMAN = 101
FONT_TIMES_ITALIC = 102
FONT_TIMES_BOLD = 103
FONT_TIMES_BOLDITALIC = 104
FONT_HELVETICA = 105
FONT_HELVETICA_OBLIQUE = 106
FONT_HELVETICA_BOLD = 107
FONT_HELVETICA_BOLDOBLIQUE = 108
FONT_COURIER = 109
FONT_COURIER_OBLIQUE = 110
FONT_COURIER_BOLD = 111
FONT_COURIER_BOLDOBLIQUE = 112
FONT_SYMBOL = 113
FONT_BOOKMAN_LIGHT = 114
FONT_BOOKMAN_LIGHTITALIC = 115
FONT_BOOKMAN_DEMI = 116
FONT_BOOKMAN_DEMIITALIC = 117
FONT_NEWCENTURYSCHLBK_ROMAN = 118
FONT_NEWCENTURYSCHLBK_ITALIC = 119
FONT_NEWCENTURYSCHLBK_BOLD = 120
FONT_NEWCENTURYSCHLBK_BOLDITALIC = 121
FONT_AVANTGARDE_BOOK = 122
FONT_AVANTGARDE_BOOKOBLIQUE = 123
FONT_AVANTGARDE_DEMI = 124
FONT_AVANTGARDE_DEMIOBLIQUE = 125
FONT_PALATINO_ROMAN = 126
FONT_PALATINO_ITALIC = 127
FONT_PALATINO_BOLD = 128
FONT_PALATINO_BOLDITALIC = 129
FONT_ZAPFCHANCERY_MEDIUMITALIC = 130
FONT_ZAPFDINGBATS = 131

PATH_STOP      = 0x00
PATH_MOVETO    = 0x01
PATH_LINETO    = 0x02
PATH_CURVE3    = 0x03
PATH_CURVE4    = 0x04
PATH_CLOSEPOLY = 0x4f

MPL_SUPPRESS_CLEAR = 1
MPL_POSTPONE_UPDATE = 2

# GR3 functions
include("gr3.jl")

const gr3 = GR.GR3

# Convenience functions
include("jlgr.jl")

figure(; kwargs...) = jlgr.figure(; kwargs...)
hold(flag) = jlgr.hold(flag)
subplot(m, n, p) = jlgr.subplot(m, n, p)
plot(args...; kwargs...) = jlgr.plot(args...; kwargs...)
oplot(args...; kwargs...) = jlgr.oplot(args...; kwargs...)
semilogx(args...; kwargs...) = jlgr.plot(args...; kwargs..., xlog=true)
semilogy(args...; kwargs...) = jlgr.plot(args...; kwargs..., ylog=true)
loglog(args...; kwargs...) = jlgr.plot(args...; kwargs..., xlog=true, ylog=true)
scatter(args...; kwargs...) = jlgr.scatter(args...; kwargs...)
stem(args...; kwargs...) = jlgr.stem(args...; kwargs...)
histogram(x; kwargs...) = jlgr.histogram(x; kwargs...)
contour(args...; kwargs...) = jlgr.contour(args...; kwargs...)
contourf(args...; kwargs...) = jlgr.contourf(args...; kwargs...)
wireframe(args...; kwargs...) = jlgr.wireframe(args...; kwargs...)
surface(args...; kwargs...) = jlgr.surface(args...; kwargs...)
plot3(args...; kwargs...) = jlgr.plot3(args...; kwargs...)
scatter3(args...; kwargs...) = jlgr.scatter3(args...; kwargs...)
title(s) = jlgr.title(s)
xlabel(s) = jlgr.xlabel(s)
ylabel(s) = jlgr.ylabel(s)
legend(args...; kwargs...) = jlgr.legend(args...; kwargs...)
xlim(a) = jlgr.xlim(a)
ylim(a) = jlgr.ylim(a)
savefig(filename) = jlgr.savefig(filename)
meshgrid(vx, vy) = jlgr.meshgrid(vx, vy)
meshgrid(vx, vy, vz) = jlgr.meshgrid(vx, vy, vz)
peaks(n...) = jlgr.peaks(n...)
imshow(I; kwargs...) = jlgr.imshow(I; kwargs...)
isosurface(V; kwargs...) = jlgr.isosurface(V; kwargs...)
cart2sph(x, y, z) = jlgr.cart2sph(x, y, z)
sph2cart(θ, ϕ, r) = jlgr.sph2cart(θ, ϕ, r)
polar(args...; kwargs...) = jlgr.polar(args...; kwargs...)
trisurf(args...; kwargs...) = jlgr.trisurf(args...; kwargs...)

type SVG
   s::Array{UInt8}
end
@compat Base.show(io::IO, ::MIME"image/svg+xml", x::SVG) = write(io, x.s)

type PNG
   s::Array{UInt8}
end
@compat Base.show(io::IO, ::MIME"image/png", x::PNG) = write(io, x.s)

type HTML
   s::AbstractString
end
@compat Base.show(io::IO, ::MIME"text/html", x::HTML) = print(io, x.s)

function _readfile(path)
    data = Array(UInt8, filesize(path))
    s = open(path, "r")
    bytestring(read!(s, data))
end

function isinline()
    global mime_type
    return !(mime_type in (None, "mov"))
end

function startserver()
    global msgs

    @eval import WebSockets
    @eval import HttpServer

    msgs = []
    app = WebSockets.WebSocketHandler() do req, client
        while true
            msg = WebSockets.read(client)
            if startswith(bytestring(msg), "ready")
                if length(msgs) != 0
                    WebSockets.write(client, msgs[1])
                    shift!(msgs)
                else
                    WebSockets.write(client, "busy")
                end
            end
        end
    end

    server = HttpServer.Server(app)
    @async begin
        HttpServer.run(server, 8889)
    end

    if !isfile("gr.js")
        symlink(joinpath(dirname(@__FILE__), "gr.js"), "gr.js")
    end

    return HTML("""\
<canvas id="canvas" width="600" height="450"></canvas>\
<script type="text/javascript" src="gr.js"></script>\
<script>GR.ready(\
  function() {\
    var ws = new WebSocket("ws://localhost:8889/");\
    ws.onopen = function() {\
      ws.send("ready");\
    };\
    ws.onmessage = function(ev) {\
      if (ev.data == "busy") {\
        setTimeout(function() {ws.send("ready");}, 10);\
      } else {\
        gr_clearws();\
        gr_drawgraphics(window.atob(ev.data));\
        ws.send("ready");\
      };\
    };\
  }\
);</script>""")
end

function inline(mime="svg", scroll=true)
    global mime_type, figure_count, msgs
    if mime_type != mime
        if mime == "iterm"
            ENV["GKS_WSTYPE"] = "pdf"
        elseif mime == "js"
            ENV["GKS_WSTYPE"] = "nul"
        else
            ENV["GKS_WSTYPE"] = mime
        end
        emergencyclosegks()
        mime_type = mime
        if mime == "js"
            startserver()
        end
    end
    figure_count = scroll ? None : 0
    mime_type
end

function show()
    global mime_type, figure_count, msgs

    emergencyclosegks()
    if mime_type == "svg"
        content = SVG(_readfile("gks.svg"))
        return content
    elseif mime_type == "png"
        content = PNG(_readfile("gks.png"))
        return content
    elseif mime_type == "mov"
        content = HTML(string("""<video autoplay controls><source type="video/mp4" src="data:video/mp4;base64,""", base64encode(open(read,"gks.mov")),""""></video>"""))
        return content
    elseif mime_type == "iterm"
        content = string("\033]1337;File=inline=1;height=24;preserveAspectRatio=0:", base64encode(open(read,"gks.pdf")), "\a")
        if figure_count != None
            figure_count += 1
            (figure_count > 1) && print("\e[24A")
        end
        println(content)
        return nothing
    elseif mime_type == "js"
        if msgs != None
            endgraphics()
            push!(msgs, Base.base64encode(getgraphics()))
        end
    end
    return None
end

function setregenflags(flags=0)
  ccall( (:gr_setregenflags, libGR),
        Void,
        (Int32, ),
        flags)
end

function inqregenflags()
  flags = ccall( (:gr_inqregenflags, libGR),
                Int32,
                ()
                )
  return flags
end

function savestate()
  ccall( (:gr_savestate, libGR),
        Void,
        ()
        )
end

function restorestate()
  ccall( (:gr_restorestate, libGR),
        Void,
        ()
        )
end

function selectcontext(context::Int)
  ccall( (:gr_selectcontext, libGR),
        Void,
        (Int32, ),
        context)
end

function uselinespec(linespec)
  return ccall( (:gr_uselinespec, libGR),
               Int32,
               (Ptr{Cchar}, ),
               linespec)
end

function trisurface(x, y, z)
  nx = length(x)
  ny = length(y)
  nz = length(z)
  n = min(nx, ny, nz)
  ccall( (:gr_trisurface, libGR),
        Void,
        (Int32, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}),
        n, convert(Vector{Float64}, x), convert(Vector{Float64}, y), convert(Vector{Float64}, z))
end

function gradient(x, y, z)
  nx = length(x)
  ny = length(y)
  nz = length(z)
  if ndims(z) == 1
    out_of_bounds = nz != nx * ny
  elseif ndims(z) == 2
    out_of_bounds = size(z)[1] != nx || size(z)[2] != ny
  else
    out_of_bounds = true
  end
  if !out_of_bounds
    if ndims(z) == 2
      z = reshape(z, nx * ny)
    end
    u = Cdouble[1 : nx*ny ;]
    v = Cdouble[1 : nx*ny ;]
    ccall( (:gr_gradient, libGR),
          Void,
          (Int32, Int32, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}, Ptr{Cdouble}, Ptr{Cdouble}),
          nx, ny, convert(Vector{Float64}, x), convert(Vector{Float64}, y), convert(Vector{Float64}, z), u, v)
    return u, v
  else
    return [], []
  end
end

function quiver(x, y, u, v, color::Bool=false)
  nx = length(x)
  ny = length(y)
  nu = length(u)
  nv = length(v)
  if ndims(u) == 1
    out_of_bounds = nu != nx * ny
  elseif ndims(u) == 2
    out_of_bounds = size(u)[1] != nx || size(u)[2] != ny
  else
    out_of_bounds = true
  end
  if !out_of_bounds
    if ndims(v) == 1
      out_of_bounds = nv != nx * ny
    elseif ndims(v) == 2
      out_of_bounds = size(v)[1] != nx || size(v)[2] != ny
    else
      out_of_bounds = true
    end
  end
  if !out_of_bounds
    if ndims(u) == 2
      u = reshape(u, nx * ny)
    end
    if ndims(v) == 2
      v = reshape(v, nx * ny)
    end
    ccall( (:gr_quiver, libGR),
          Void,
          (Int32, Int32, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}, Ptr{Float64}, Int32),
          nx, ny, convert(Vector{Float64}, x), convert(Vector{Float64}, y), convert(Vector{Float64}, u), convert(Vector{Float64}, v), convert(Int32, color))
  else
    println("Arrays have incorrect length or dimension.")
  end
end

end # module
